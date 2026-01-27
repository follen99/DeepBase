# src/deepbase/main.py

import os
import typer
import fnmatch
from rich.console import Console
from rich.progress import Progress
import tomli
import chardet
# --- NUOVI IMPORT PER LA VERSIONE ---
from importlib.metadata import version as get_package_version, PackageNotFoundError
from typing import List, Dict, Any, Set, Optional

from deepbase.toon import generate_toon_representation
from deepbase.parsers import get_document_structure

# --- CONFIGURAZIONI (Invariate) ---
DEFAULT_CONFIG = {
    "ignore_dirs": {
        "__pycache__", ".git", ".idea", ".vscode", "venv", ".venv", "env",
        ".env", "node_modules", "build", "dist", "target", "out", "bin",
        "obj", "logs", "tmp", "eggs", ".eggs", ".pytest_cache", ".tox",
        "site", "*.egg-info", "coverage"
    },
    "significant_extensions": {
        ".py", ".java", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss", ".sql",
        ".md", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat", "Dockerfile",
        ".dockerignore", ".gitignore", "requirements.txt", "pom.xml", "gradlew",
        "pyproject.toml", "setup.py", "package.json", "tsconfig.json",
        ".tex", ".bib", ".sty", ".cls"
    }
}

app = typer.Typer(
    name="deepbase",
    help="Analyzes a project or file and creates a unified context document for an LLM.",
    add_completion=False
)
console = Console()

# --- HELPER FUNCTIONS (Invariate) ---
def load_config(root_dir: str) -> Dict[str, Any]:
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
    _, ext = os.path.splitext(file_path) # Corretto os.path.splitext(file_name) -> file_path per sicurezza
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

def matches_focus(file_path: str, root_dir: str, focus_patterns: List[str]) -> bool:
    if not focus_patterns:
        return False
    rel_path = os.path.relpath(file_path, root_dir)
    rel_path_fwd = rel_path.replace(os.sep, '/')
    for pattern in focus_patterns:
        clean_pattern = pattern.replace(os.sep, '/')
        if fnmatch.fnmatch(rel_path_fwd, clean_pattern):
            return True
        if clean_pattern in rel_path_fwd:
            return True
    return False

def load_focus_patterns_from_file(file_path: str) -> List[str]:
    patterns = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
        except Exception as e:
            console.print(f"[bold yellow]Warning:[/bold yellow] Could not read focus file '{file_path}': {e}")
    else:
        console.print(f"[bold yellow]Warning:[/bold yellow] Focus file '{file_path}' not found.")
    return patterns


# --- FUNZIONE CALLBACK PER VERSIONE ---
def version_callback(value: bool):
    if value:
        try:
            v = get_package_version("deepbase")
            console.print(f"DeepBase version: [bold cyan]{v}[/bold cyan]")
        except PackageNotFoundError:
            console.print("DeepBase version: [yellow]unknown (editable/dev mode)[/yellow]")
        raise typer.Exit()

# --- MAIN COMMAND ---

@app.command()
def create(
    # Nota: Ho reso 'target' facoltativo (Optional) nel type hint solo per evitare errori 
    # statici se non viene passato quando si usa --version, 
    # ma Typer lo gestirà comunque come richiesto se non eseguiamo la callback.
    target: str = typer.Argument(
        None, # Default a None per permettere a --version di funzionare senza target
        help="The file or directory to scan."
    ),
    
    # --- FLAG VERSIONE ---
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", 
        callback=version_callback, 
        is_eager=True, # IMPORTANTE: Processa questo flag prima di controllare gli argomenti required
        help="Show the application version and exit."
    ),

    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file."),
    
    # NOTA: Ho cambiato lo short flag di verbose da -v a -V per lasciare -v alla version
    verbose: bool = typer.Option(False, "--verbose", "-V", help="Show detailed output."),
    
    include_all: bool = typer.Option(False, "--all", "-a", help="Include full content of ALL files."),
    toon_mode: bool = typer.Option(False, "--toon", "-t", help="Use 'Skeleton' mode for non-focused files."),
    focus: Optional[List[str]] = typer.Option(None, "--focus", "-f", help="Pattern to focus on."),
    focus_file: Optional[str] = typer.Option(None, "--focus-file", "-ff", help="Path to focus patterns file.")
):
    """
    Analyzes a directory OR a single file.
    Hybrid workflow with Context Skeleton + Focused Content.
    """
    
    # Se target è None (succede solo se uno lancia deepbase senza argomenti e senza --version)
    if target is None:
        # Mostra help ed esci
        ctx = typer.get_current_context()
        console.print("[red]Error: Missing argument 'TARGET'.[/red]")
        console.print(ctx.get_help())
        raise typer.Exit(code=1)

    if not os.path.exists(target):
        console.print(f"[bold red]Error:[/bold red] Target not found: '{target}'")
        raise typer.Exit(code=1)

    # --- LOGICA FOCUS MERGE ---
    active_focus_patterns = []
    if focus: active_focus_patterns.extend(focus)
    if focus_file:
        file_patterns = load_focus_patterns_from_file(focus_file)
        if file_patterns: active_focus_patterns.extend(file_patterns)
    active_focus_patterns = list(set(active_focus_patterns))

    console.print(f"[bold green]Analyzing '{target}'...[/bold green]")
    
    if toon_mode and active_focus_patterns:
         console.print(f"[yellow]Hybrid Mode active: TOON + Focus on {len(active_focus_patterns)} patterns.[/yellow]")
    elif toon_mode:
        console.print("[yellow]TOON Mode active: Minimalist output.[/yellow]")

    # --- STYLE CONFIGURATION ---
    if toon_mode:
        def fmt_header(title): return f"### {title}\n\n"
        def fmt_file_start(path): return f"> FILE: {path}\n"
        def fmt_file_end(path):   return "\n"
        def fmt_separator():      return "" 
    else:
        def fmt_header(title): 
            line = "="*80 
            return f"{line}\n### {title} ###\n{line}\n\n"
        def fmt_file_start(path): return f"--- START OF FILE: {path} ---\n\n"
        def fmt_file_end(path):   return f"\n\n--- END OF FILE: {path} ---\n"
        def fmt_separator():      return "-" * 40 + "\n\n"

    try:
        with open(output, "w", encoding="utf-8") as outfile:
            
            # CASE 1: SINGLE FILE
            if os.path.isfile(target):
                filename = os.path.basename(target)
                outfile.write(f"# File Structure Analysis: {filename}\n\n")
                content = read_file_content(target)
                structure = get_document_structure(target, content)
                outfile.write(fmt_header("DOCUMENT STRUCTURE (Outline)"))
                outfile.write(structure or "N/A")
                outfile.write("\n\n")
                if include_all or toon_mode:
                     section = "SEMANTIC SKELETONS (TOON)" if toon_mode else "FILE CONTENT"
                     outfile.write(fmt_header(section))
                     outfile.write(fmt_file_start(filename))
                     if toon_mode: outfile.write(generate_toon_representation(target, content))
                     else: outfile.write(content)
                     outfile.write(fmt_file_end(filename))

            # CASE 2: DIRECTORY
            elif os.path.isdir(target):
                config = load_config(target)
                outfile.write(f"# Project Context: {os.path.basename(os.path.abspath(target))}\n\n")
                
                # 1. Structure
                outfile.write(fmt_header("PROJECT STRUCTURE"))
                directory_tree = generate_directory_tree(target, config)
                outfile.write(directory_tree)
                outfile.write("\n\n")

                # 2. Content Generation
                if include_all or toon_mode or active_focus_patterns:
                    section_title = "FILE CONTENTS (HYBRID)" if (toon_mode and active_focus_patterns) else \
                                    ("SEMANTIC SKELETONS (TOON)" if toon_mode else "FILE CONTENTS")
                    outfile.write(fmt_header(section_title))
                    files = get_all_significant_files(target, config)
                    
                    with Progress(console=console) as progress:
                        task = progress.add_task("[cyan]Processing...", total=len(files))
                        for fpath in files:
                            rel_path = os.path.relpath(fpath, target).replace('\\', '/')
                            is_in_focus = active_focus_patterns and matches_focus(fpath, target, active_focus_patterns)
                            should_write_full = include_all or is_in_focus
                            should_write_toon = toon_mode and not should_write_full
                            
                            if not should_write_full and not should_write_toon:
                                progress.update(task, advance=1)
                                continue

                            progress.update(task, advance=1, description=f"[cyan]{rel_path}[/cyan]")
                            marker = ""
                            if is_in_focus and toon_mode: marker = " [FOCUSED - FULL CONTENT]"
                            
                            outfile.write(fmt_file_start(rel_path + marker))
                            content = read_file_content(fpath)
                            if should_write_full: outfile.write(content)
                            elif should_write_toon: outfile.write(generate_toon_representation(fpath, content))
                            outfile.write(fmt_file_end(rel_path))
                            outfile.write(fmt_separator())
                else:
                     console.print("[dim]Note: Only directory tree generated. Use --toon, --all, or --focus to see content.[/dim]")

        console.print(f"\n[bold green]✓ SUCCESS[/bold green]: Context created in [cyan]'{output}'[/cyan]")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()