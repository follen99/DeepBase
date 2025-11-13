# src/deepbase/main.py
"""
This module contains the core logic for the DeepBase CLI tool.

It provides functionalities to scan a project directory, generate a structured
overview, and consolidate the content of significant files into a single
context file for Large Language Models (LLMs).
"""

import os
import typer
from rich.console import Console
from rich.progress import Progress
import tomli
import chardet
from typing import List, Dict, Any, Set

# --- CONSTANTS AND CONFIGURATION ---

# Default configuration for ignored directories and significant file extensions.
# This is used as a fallback if no .deepbase.toml file is found.
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

# --- TOOL INITIALIZATION ---

# Typer application instance for the CLI.
app = typer.Typer(
    name="deepbase",
    help="Analyzes a project directory and creates a unified context document for an LLM.",
    add_completion=False
)
# Rich Console instance for beautiful terminal output.
console = Console()


def load_config(root_dir: str) -> Dict[str, Any]:
    """
    Loads configuration from a .deepbase.toml file in the project root.

    If the file is not found or is invalid, it falls back to DEFAULT_CONFIG.
    User-defined lists are merged with the default ones.

    Args:
        root_dir: The root directory of the project being scanned.

    Returns:
        A dictionary containing the final configuration settings.
    """
    config_path = os.path.join(root_dir, ".deepbase.toml")
    config = DEFAULT_CONFIG.copy()
    
    if os.path.exists(config_path):
        console.print(f"[bold cyan]Found configuration file: '.deepbase.toml'[/bold cyan]")
        try:
            with open(config_path, "rb") as f:
                user_config = tomli.load(f)
            
            # Merge user config with defaults by updating the sets
            config["ignore_dirs"].update(user_config.get("ignore_dirs", []))
            config["significant_extensions"].update(user_config.get("significant_extensions", []))
            console.print("[green]Custom configuration loaded successfully.[/green]")

        except tomli.TOMLDecodeError as e:
            console.print(f"[bold red]Error parsing .deepbase.toml:[/bold red] {e}")
            console.print("[yellow]Using default configuration.[/yellow]")
    
    return config


def is_significant_file(file_path: str, significant_extensions: Set[str]) -> bool:
    """
    Checks if a file is significant based on its name or extension.

    Args:
        file_path: The full path to the file.
        significant_extensions: A set of filenames and extensions to check against.

    Returns:
        True if the file is deemed significant, False otherwise.
    """
    file_name = os.path.basename(file_path)
    if file_name in significant_extensions:
        return True
    _, ext = os.path.splitext(file_name)
    return ext in significant_extensions


def generate_directory_tree(root_dir: str, config: Dict[str, Any]) -> str:
    """
    Generates a text representation of the folder structure.

    This function walks the directory and builds a string that visually
    represents the hierarchy of folders and significant files.

    Args:
        root_dir: The root directory of the project.
        config: The configuration dictionary containing ignore lists.

    Returns:
        A multi-line string representing the project's directory tree.
    """
    tree_str = f"Project Structure in: {os.path.abspath(root_dir)}\n\n"
    ignore_dirs = config["ignore_dirs"]
    significant_exts = config["significant_extensions"]

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Filter out ignored directories in-place
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
    """
    Gets a list of all significant files to be included in the context.

    This function walks the directory tree and collects the paths of all files
    that are considered significant according to the configuration.

    Args:
        root_dir: The root directory of the project.
        config: The configuration dictionary.

    Returns:
        A list of absolute paths to the significant files.
    """
    significant_files = []
    ignore_dirs = config["ignore_dirs"]
    significant_exts = config["significant_extensions"]

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Filter out ignored directories in-place
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        
        for filename in sorted(filenames):
            file_path = os.path.join(dirpath, filename)
            if is_significant_file(file_path, significant_exts):
                significant_files.append(file_path)

    return significant_files


@app.command()
def create(
    directory: str = typer.Argument(..., help="The root directory of the project to scan."),
    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file that will contain the context."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output, including ignored files.")
):
    """
    Analyzes a project directory and creates a unified context file for an LLM.

    This is the main command of the DeepBase CLI. It orchestrates the process of
    loading configuration, scanning the directory, generating the structure tree,
    and concatenating the content of all significant files into a single output file.
    """
    if not os.path.isdir(directory):
        console.print(f"[bold red]Error:[/bold red] The specified directory does not exist: '{directory}'")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Starting scan of '{directory}'...[/bold green]")
    
    config = load_config(directory)
    
    try:
        with open(output, "w", encoding="utf-8") as outfile:
            # Step 1: Write the main header
            outfile.write(f"# Project Context: {os.path.basename(os.path.abspath(directory))}\n\n")
            
            # Step 2: Generate and write the directory structure
            outfile.write("="*80 + "\n### PROJECT STRUCTURE ###\n" + "="*80 + "\n\n")
            directory_tree = generate_directory_tree(directory, config)
            outfile.write(directory_tree)
            outfile.write("\n\n")

            # Step 3: Find all significant files and write their contents
            outfile.write("="*80 + "\n### FILE CONTENTS ###\n" + "="*80 + "\n\n")
            
            significant_files = get_all_significant_files(directory, config)

            with Progress(console=console) as progress:
                task = progress.add_task("[cyan]Analyzing files...", total=len(significant_files))

                for file_path in significant_files:
                    relative_path = os.path.relpath(file_path, directory).replace('\\', '/')
                    progress.update(task, advance=1, description=f"[cyan]Analyzing: {relative_path}[/cyan]")

                    outfile.write(f"--- START OF FILE: {relative_path} ---\n\n")
                    try:
                        with open(file_path, "rb") as fb:
                            raw_data = fb.read()
                        
                        # Detect encoding to prevent read errors
                        detection = chardet.detect(raw_data)
                        encoding = detection['encoding'] if detection['encoding'] else 'utf-8'
                        
                        # Read and write content with robust error handling for encoding
                        content = raw_data.decode(encoding, errors="replace")
                        outfile.write(content)

                    except Exception as e:
                        outfile.write(f"!!! Error while reading file: {e} !!!\n")
                    
                    outfile.write(f"\n\n--- END OF FILE: {relative_path} ---\n\n")
                    outfile.write("-" * 40 + "\n\n")
        
        console.print(f"\n[bold green]✓ SUCCESS[/bold green]: Context successfully created in file: [cyan]'{output}'[/cyan]")

    except IOError as e:
        console.print(f"\n[bold red]Error writing to output file:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)


# Entry point for running the script directly
if __name__ == "__main__":
    app()