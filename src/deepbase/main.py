# src/deepbase/main.py

import os
import typer
from rich.console import Console
from rich.progress import Progress
import tomli
import chardet
from typing import List, Dict, Any, Set

from deepbase.parsers import get_document_structure

# --- CONSTANTS AND CONFIGURATION ---
# (Il blocco DEFAULT_CONFIG rimane invariato...)
DEFAULT_CONFIG = {
    "ignore_dirs": {
        "__pycache__", ".git", ".idea", ".vscode", "venv", ".venv", "env",
        ".env", "node_modules", "build", "dist", "target", "out", "bin",
        "obj", "logs", "tmp", "eggs", ".eggs", ".pytest_cache", ".tox",
        "site", "*.egg-info",
    },
    "significant_extensions": {
        ".py", ".java", ".js", ".ts", ".html", ".css", ".scss", ".sql",
        ".md", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat", "Dockerfile",
        ".dockerignore", ".gitignore", "requirements.txt", "pom.xml", "gradlew",
        "pyproject.toml", "setup.py",
    }
}

app = typer.Typer(
    name="deepbase",
    help="Analyzes a project or file and creates a unified context document for an LLM.",
    add_completion=False
)
console = Console()

# (Le funzioni helper load_config, is_significant_file, generate_directory_tree, 
# get_all_significant_files, read_file_content rimangono invariate...)

def load_config(root_dir: str) -> Dict[str, Any]:
    """Loads configuration from .deepbase.toml if available."""
    config_path = os.path.join(root_dir, ".deepbase.toml")
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, "rb") as f:
                user_config = tomli.load(f)
            config["ignore_dirs"].update(user_config.get("ignore_dirs", []))
            config["significant_extensions"].update(user_config.get("significant_extensions", []))
        except tomli.TOMLDecodeError:
            pass
    return config

def is_significant_file(file_path: str, significant_extensions: Set[str]) -> bool:
    file_name = os.path.basename(file_path)
    if file_name in significant_extensions: return True
    _, ext = os.path.splitext(file_name)
    return ext in significant_extensions

def generate_directory_tree(root_dir: str, config: Dict[str, Any]) -> str:
    tree_str = f"Project Structure in: {os.path.abspath(root_dir)}\n\n"
    ignore_dirs = config["ignore_dirs"]
    significant_exts = config["significant_extensions"]
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        tree_str += f"{indent}📂 {os.path.basename(dirpath) or os.path.basename(os.path.abspath(root_dir))}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        for f in sorted(filenames):
            if is_significant_file(os.path.join(dirpath, f), significant_exts):
                tree_str += f"{sub_indent}📄 {f}\n"
    return tree_str

def get_all_significant_files(root_dir: str, config: Dict[str, Any]) -> List[str]:
    significant_files = []
    ignore_dirs = config["ignore_dirs"]
    significant_exts = config["significant_extensions"]
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        for filename in sorted(filenames):
            file_path = os.path.join(dirpath, filename)
            if is_significant_file(file_path, significant_exts):
                significant_files.append(file_path)
    return significant_files

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, "rb") as fb:
            raw_data = fb.read()
        detection = chardet.detect(raw_data)
        encoding = detection['encoding'] if detection['encoding'] else 'utf-8'
        return raw_data.decode(encoding, errors="replace")
    except Exception as e:
        return f"!!! Error reading file: {e} !!!"

@app.command()
def create(
    target: str = typer.Argument(..., help="The file or directory to scan."),
    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output."),
    include_all: bool = typer.Option(False, "--all", "-a", help="If target is a file, append full content after structure.")
):
    """
    Analyzes a directory OR a single file.
    
    If TARGET is a DIRECTORY: Generates a full project context (tree + content).
    If TARGET is a FILE: Generates ONLY the structure outline by default. Use --all to include content.
    """
    if not os.path.exists(target):
        console.print(f"[bold red]Error:[/bold red] Target not found: '{target}'")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Analyzing '{target}'...[/bold green]")

    try:
        with open(output, "w", encoding="utf-8") as outfile:
            
            # --- CASE 1: SINGLE FILE ---
            if os.path.isfile(target):
                filename = os.path.basename(target)
                
                outfile.write(f"# File Structure Analysis: {filename}\n\n")
                
                # 1. Read Content (needed for structure parsing)
                content = read_file_content(target)
                
                # 2. Extract and Write Structure
                structure = get_document_structure(target, content)
                
                outfile.write("="*80 + "\n### DOCUMENT STRUCTURE (Outline) ###\n" + "="*80 + "\n\n")
                if structure:
                    outfile.write(structure)
                else:
                    outfile.write("(Structure extraction not available for this file type)")
                outfile.write("\n\n")

                # 3. Write Content ONLY if requested
                if include_all:
                    outfile.write("="*80 + "\n### FILE CONTENT ###\n" + "="*80 + "\n\n")
                    outfile.write(f"--- START OF FILE: {filename} ---\n\n")
                    outfile.write(content)
                    outfile.write(f"\n\n--- END OF FILE: {filename} ---\n")
                else:
                    console.print("[dim]Note: Only structure was generated. Use --all to include full content.[/dim]")

            # --- CASE 2: DIRECTORY ---
            elif os.path.isdir(target):
                # Directory scan implies full context usually, so include_all is implicitly True/ignored
                config = load_config(target)
                
                outfile.write(f"# Project Context: {os.path.basename(os.path.abspath(target))}\n\n")
                
                # 1. Directory Tree
                outfile.write("="*80 + "\n### PROJECT STRUCTURE ###\n" + "="*80 + "\n\n")
                directory_tree = generate_directory_tree(target, config)
                outfile.write(directory_tree)
                outfile.write("\n\n")

                # 2. Files Content
                outfile.write("="*80 + "\n### FILE CONTENTS ###\n" + "="*80 + "\n\n")
                files = get_all_significant_files(target, config)
                
                with Progress(console=console) as progress:
                    task = progress.add_task("[cyan]Processing...", total=len(files))
                    for fpath in files:
                        rel_path = os.path.relpath(fpath, target).replace('\\', '/')
                        progress.update(task, advance=1, description=f"[cyan]{rel_path}[/cyan]")
                        
                        outfile.write(f"--- START OF FILE: {rel_path} ---\n\n")
                        outfile.write(read_file_content(fpath))
                        outfile.write(f"\n\n--- END OF FILE: {rel_path} ---\n")
                        outfile.write("-" * 40 + "\n\n")

        console.print(f"\n[bold green]✓ SUCCESS[/bold green]: Context created in [cyan]'{output}'[/cyan]")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()