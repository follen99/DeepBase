# src/deepbase/main.py

import os
import typer
import fnmatch
import math
from rich.console import Console
from rich.progress import Progress
import tomli
import chardet
from importlib.metadata import version as get_package_version, PackageNotFoundError
from typing import List, Dict, Any, Set, Optional, Tuple

from deepbase.toon import generate_toon_representation, generate_database_focused
from deepbase.parsers import get_document_structure
from deepbase.database import is_sqlite_database, get_database_schema, generate_database_context_full

# --- CONFIGURAZIONI ---

DEFAULT_CONFIG = {
    "ignore_dirs": {
        "__pycache__", ".git", ".idea", ".vscode", "venv", ".venv", "env",
        ".env", "node_modules", "build", "dist", "target", "out", "bin",
        "obj", "logs", "tmp", "eggs", ".eggs", ".pytest_cache", ".tox",
        "site", "*.egg-info", "coverage", ".next", ".nuxt", ".output",
        "ios", "android"
    },
    "ignore_files": {
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
        "poetry.lock", "Pipfile.lock", "composer.lock", ".DS_Store", "Thumbs.db"
    },
    "significant_extensions": {
        ".py", ".java", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss", ".sql",
        ".md", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat", "Dockerfile",
        ".dockerignore", ".gitignore", "requirements.txt", "pom.xml", "gradlew",
        "pyproject.toml", "setup.py", "package.json", "tsconfig.json",
        ".tex", ".bib", ".sty", ".cls",
        ".db", ".sqlite", ".sqlite3", ".db3"
    }
}

EPILOG_TEXT = """
[bold]Documentation:[/] https://follen99.github.io/DeepBase/
[bold]Repository:[/] https://github.com/follen99/DeepBase
[bold]Issues:[/] https://github.com/follen99/DeepBase/issues
[bold]PyPI:[/] https://pypi.org/project/deepbase/

[italic]DeepBase scans your project and consolidates it for LLM context analysis.[/italic]
"""

app = typer.Typer(
    name="deepbase",
    add_completion=False,
    rich_markup_mode="rich"
)
console = Console()

# --- UTILS ---

def load_config(root_dir: str) -> Dict[str, Any]:
    config_path = os.path.join(root_dir, ".deepbase.toml")
    config = DEFAULT_CONFIG.copy()
    config["ignore_dirs"] = set(config["ignore_dirs"])
    config["ignore_files"] = set(config["ignore_files"])
    config["significant_extensions"] = set(config["significant_extensions"])

    if os.path.exists(config_path):
        try:
            with open(config_path, "rb") as f:
                user_config = tomli.load(f)
            config["ignore_dirs"].update(user_config.get("ignore_dirs", []))
            config["ignore_files"].update(user_config.get("ignore_files", []))
            config["significant_extensions"].update(user_config.get("significant_extensions", []))
        except tomli.TOMLDecodeError:
            pass
    return config

def estimate_tokens(size_bytes: int) -> str:
    if size_bytes == 0: return "0t"
    tokens = math.ceil(size_bytes / 4)
    if tokens < 1000:
        return f"~{tokens}t"
    elif tokens < 1000000:
        return f"~{tokens/1000:.1f}k t"
    else:
        return f"~{tokens/1000000:.1f}M t"

def is_significant_file(file_path: str, config: Dict[str, Any], output_file_abs: str = None) -> bool:
    file_name = os.path.basename(file_path)
    
    # Check 1: Esclusione del file di output corrente (tramite path assoluto)
    if output_file_abs and os.path.abspath(file_path) == output_file_abs:
        return False

    # Check 2 (NUOVO): Esclusione per nome. 
    # Se nella cartella target esiste un file che si chiama come il file di output 
    # (es: "llm_context.md"), lo ignoriamo a prescindere dal path.
    if output_file_abs and file_name == os.path.basename(output_file_abs):
        return False

    # Check 3: Esclusione file spazzatura (lockfiles, etc definita in config)
    if file_name in config["ignore_files"]:
        return False

    significant_extensions = config["significant_extensions"]
    
    if file_name in significant_extensions: 
        return True
        
    _, ext = os.path.splitext(file_path)
    if ext in significant_extensions:
        return True

    if is_sqlite_database(file_path):
        return True
        
    return False

def calculate_project_stats(root_dir: str, config: Dict[str, Any], output_file_abs: str) -> int:
    total_size = 0
    ignore_dirs = config["ignore_dirs"]
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        for f in filenames:
            fpath = os.path.join(dirpath, f)
            if is_significant_file(fpath, config, output_file_abs):
                try:
                    total_size += os.path.getsize(fpath)
                except OSError:
                    pass
    return total_size

# --- ALBERO DELLE DIRECTORY ---

def _generate_tree_recursive(
    current_path: str,
    prefix: str,
    config: Dict[str, Any],
    total_project_size: int,
    output_file_abs: str
) -> Tuple[str, int]:
    """
    Ritorna una tupla: (stringa_visuale_albero, dimensione_totale_bytes_subtree).
    """
    output_str = ""
    subtree_size = 0
    
    try:
        items = sorted(os.listdir(current_path))
    except PermissionError:
        return "", 0

    filtered_items = []
    for item in items:
        full_path = os.path.join(current_path, item)
        is_dir = os.path.isdir(full_path)
        
        if is_dir:
            if item not in config["ignore_dirs"] and not item.startswith('.'):
                filtered_items.append((item, True))
        else:
            if is_significant_file(full_path, config, output_file_abs):
                filtered_items.append((item, False))

    for i, (name, is_dir) in enumerate(filtered_items):
        is_last = (i == len(filtered_items) - 1)
        full_path = os.path.join(current_path, name)
        connector = "└── " if is_last else "├── "
        
        if is_dir:
            # Ricorsione: ottengo prima il contenuto e la dimensione della sottocartella
            extension = "    " if is_last else "│   "
            sub_tree_str, sub_dir_size = _generate_tree_recursive(
                full_path, 
                prefix + extension, 
                config, 
                total_project_size,
                output_file_abs
            )
            
            subtree_size += sub_dir_size
            
            # Genero stats cartella
            folder_stats = ""
            if total_project_size > 0 and sub_dir_size > 0:
                percent = (sub_dir_size / total_project_size) * 100
                token_est = estimate_tokens(sub_dir_size)
                folder_stats = f" ({percent:.1f}% | {token_est})"

            output_str += f"{prefix}{connector}📁 {name}/{folder_stats}\n"
            output_str += sub_tree_str
            
        else:
            icon = "üóÑÔ∏è " if is_sqlite_database(full_path) else "📄 "
            try:
                size = os.path.getsize(full_path)
                subtree_size += size
                
                file_stats = ""
                if total_project_size > 0 and size > 0:
                    percent = (size / total_project_size) * 100
                    token_est = estimate_tokens(size)
                    file_stats = f" ({percent:.1f}% | {token_est})"
                
                output_str += f"{prefix}{connector}{icon}{name}{file_stats}\n"
            except OSError:
                pass

    return output_str, subtree_size

def generate_directory_tree(root_dir: str, config: Dict[str, Any], output_file_abs: str) -> Tuple[str, int, int]:
    abs_root = os.path.abspath(root_dir)
    total_size = calculate_project_stats(root_dir, config, output_file_abs)
    
    tree_body, _ = _generate_tree_recursive(root_dir, "", config, total_size, output_file_abs)
    
    header = f"📁 {os.path.basename(abs_root) or '.'}/\n"
    total_tokens_est = math.ceil(total_size / 4)
    return header + tree_body, total_size, total_tokens_est

# --- CORE ---

def get_all_significant_files(root_dir: str, config: Dict[str, Any], output_file_abs: str) -> List[str]:
    significant_files = []
    ignore_dirs = config["ignore_dirs"]
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        for filename in sorted(filenames):
            file_path = os.path.join(dirpath, filename)
            if is_significant_file(file_path, config, output_file_abs):
                significant_files.append(file_path)
    return significant_files

def read_file_content(file_path: str) -> str:
    if is_sqlite_database(file_path):
        try:
            schema = get_database_schema(file_path)
            return generate_database_context_full(schema, os.path.basename(file_path))
        except Exception as e:
            return f"!!! Error reading database: {e} !!!"
    try:
        with open(file_path, "rb") as fb:
            raw_data = fb.read()
        detection = chardet.detect(raw_data)
        encoding = detection['encoding'] if detection['encoding'] else 'utf-8'
        return raw_data.decode(encoding, errors="replace")
    except Exception as e:
        return f"!!! Error reading file: {e} !!!"

def matches_focus(file_path: str, root_dir: str, focus_patterns: List[str]) -> bool:
    if not focus_patterns: return False
    rel_path = os.path.relpath(file_path, root_dir)
    rel_path_fwd = rel_path.replace(os.sep, '/')
    for pattern in focus_patterns:
        if '.db/' in pattern or '.sqlite/' in pattern:
            parts = pattern.split('/')
            if len(parts) >= 2 and any(ext in parts[0] for ext in ['.db', '.sqlite']): pass 
        clean_pattern = pattern.replace(os.sep, '/')
        if fnmatch.fnmatch(rel_path_fwd, clean_pattern): return True
        if clean_pattern in rel_path_fwd: return True
    return False

def extract_focused_tables(file_path: str, focus_patterns: List[str]) -> List[str]:
    if not is_sqlite_database(file_path): return []
    db_name = os.path.basename(file_path)
    focused_tables = []
    for pattern in focus_patterns:
        if '/' in pattern:
            db_pattern, table_name = pattern.split('/', 1)
            if fnmatch.fnmatch(db_name, db_pattern): focused_tables.append(table_name)
    return focused_tables

def load_focus_patterns_from_file(file_path: str) -> List[str]:
    patterns = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"): patterns.append(line)
        except Exception as e:
            console.print(f"[bold yellow]Warning:[/bold yellow] Could not read focus file '{file_path}': {e}")
    else:
        console.print(f"[bold yellow]Warning:[/bold yellow] Focus file '{file_path}' not found.")
    return patterns

def version_callback(value: bool):
    if value:
        try:
            v = get_package_version("deepbase")
            console.print(f"DeepBase version: [bold cyan]{v}[/bold cyan]")
        except PackageNotFoundError:
            console.print("DeepBase version: [yellow]unknown (editable/dev mode)[/yellow]")
        raise typer.Exit()

@app.command(epilog=EPILOG_TEXT, rich_help_panel="Main Commands")
def create(
    target: str = typer.Argument(None, help="The file or directory to scan."),
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit."),
    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file."),
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
    if target is None:
        console.print("[red]Error: Missing argument 'TARGET'.[/red]")
        console.print(f"\n[bold]Usage:[/bold] deepbase [OPTIONS] [TARGET]\n\nTry [cyan]deepbase --help[/cyan] for more info.")
        raise typer.Exit(code=1)

    if not os.path.exists(target):
        console.print(f"[bold red]Error:[/bold red] Target not found: '{target}'")
        raise typer.Exit(code=1)

    abs_output_path = os.path.abspath(output)
    
    active_focus_patterns = []
    if focus: active_focus_patterns.extend(focus)
    if focus_file:
        file_patterns = load_focus_patterns_from_file(focus_file)
        if file_patterns: active_focus_patterns.extend(file_patterns)
    active_focus_patterns = list(set(active_focus_patterns))

    console.print(f"[bold green]Analyzing '{target}'...[/bold green]")

    if toon_mode:
        def fmt_header(title): return f"### {title}\n\n"
        def fmt_file_start(path, icon=""): return f"> FILE: {icon}{path}\n"
        def fmt_file_end(path): return "\n"
        def fmt_separator(): return "" 
    else:
        def fmt_header(title): return f"{'='*80}\n### {title} ###\n{'='*80}\n\n"
        def fmt_file_start(path, icon=""): return f"--- START OF FILE: {icon}{path} ---\n\n"
        def fmt_file_end(path): return f"\n\n--- END OF FILE: {path} ---\n"
        def fmt_separator(): return "-" * 40 + "\n\n"

    try:
        with open(output, "w", encoding="utf-8") as outfile:
            if os.path.isfile(target):
                filename = os.path.basename(target)
                is_db = is_sqlite_database(target)
                outfile.write(f"# Analysis: {filename}\n\n")
                if is_db:
                    schema = get_database_schema(target)
                    focused_tables = extract_focused_tables(target, active_focus_patterns)
                    is_focused = bool(focused_tables) or (active_focus_patterns and any(
                        fnmatch.fnmatch(filename, p) or p in filename for p in active_focus_patterns
                    ))
                    outfile.write(fmt_header("DATABASE SCHEMA"))
                    if toon_mode and not is_focused:
                        outfile.write(generate_toon_representation(target, ""))
                    elif focused_tables:
                         outfile.write(generate_database_focused(target, focused_tables))
                    else:
                        outfile.write(generate_database_context_full(schema, filename))
                else:
                    content = read_file_content(target)
                    structure = get_document_structure(target, content)
                    outfile.write(fmt_header("STRUCTURE"))
                    outfile.write(structure or "N/A")
                    outfile.write("\n\n")
                    outfile.write(fmt_header("CONTENT"))
                    outfile.write(fmt_file_start(filename))
                    if toon_mode: outfile.write(generate_toon_representation(target, content))
                    else: outfile.write(content)
                    outfile.write(fmt_file_end(filename))

            elif os.path.isdir(target):
                config = load_config(target)
                outfile.write(f"# Project Context: {os.path.basename(os.path.abspath(target))}\n\n")
                outfile.write(fmt_header("PROJECT STRUCTURE"))
                
                tree_str, total_bytes, total_tokens = generate_directory_tree(target, config, abs_output_path)
                outfile.write(f"> Total Size: {total_bytes/1024:.2f} KB | Est. Tokens: ~{total_tokens:,}\n")
                outfile.write(tree_str)
                outfile.write("\n\n")

                if include_all or toon_mode or active_focus_patterns:
                    section_title = "FILE CONTENTS"
                    if toon_mode: section_title += " (TOON)"
                    outfile.write(fmt_header(section_title))
                    files = get_all_significant_files(target, config, abs_output_path)
                    
                    with Progress(console=console) as progress:
                        task = progress.add_task("[cyan]Processing...", total=len(files))
                        for fpath in files:
                            rel_path = os.path.relpath(fpath, target).replace('\\', '/')
                            is_db = is_sqlite_database(fpath)
                            is_in_focus = active_focus_patterns and matches_focus(fpath, target, active_focus_patterns)
                            focused_tables = []
                            if is_db:
                                focused_tables = extract_focused_tables(fpath, active_focus_patterns)
                                if focused_tables: is_in_focus = True
                            should_write_full = include_all or is_in_focus
                            should_write_toon = toon_mode and not should_write_full
                            if not should_write_full and not should_write_toon:
                                progress.update(task, advance=1)
                                continue

                            progress.update(task, advance=1, description=f"[cyan]{rel_path}[/cyan]")
                            marker = " [FOCUSED]" if (is_in_focus and toon_mode) else ""
                            icon = "üóÑÔ∏è " if is_db else ""
                            outfile.write(fmt_file_start(rel_path + marker, icon))
                            
                            if is_db:
                                if should_write_full:
                                    if focused_tables: outfile.write(generate_database_focused(fpath, focused_tables))
                                    else:
                                        schema = get_database_schema(fpath)
                                        outfile.write(generate_database_context_full(schema, os.path.basename(fpath)))
                                else: outfile.write(generate_toon_representation(fpath, ""))
                            else:
                                content = read_file_content(fpath)
                                if should_write_full: outfile.write(content)
                                elif should_write_toon: outfile.write(generate_toon_representation(fpath, content))
                            outfile.write(fmt_file_end(rel_path))
                            outfile.write(fmt_separator())
                else:
                     console.print("[dim]Directory tree generated. Use --toon, --all, or --focus for content.[/dim]")

        console.print(f"\n[bold green]✓ SUCCESS[/bold green]: Context created in [cyan]'{output}'[/cyan]")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()