# src/deepbase/main.py (AGGIORNAMENTO - sezioni modificate)
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

from deepbase.toon import generate_toon_representation, generate_database_focused
from deepbase.parsers import get_document_structure
from deepbase.database import is_sqlite_database, get_database_schema, generate_database_context_full

# --- CONFIGURAZIONI AGGIORNATE ---
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
        ".tex", ".bib", ".sty", ".cls",
        # --- DATABASE EXTENSIONS ---
        ".db", ".sqlite", ".sqlite3", ".db3"
    }
}

app = typer.Typer(
    name="deepbase",
    help="Analyzes a project or file and creates a unified context document for an LLM.",
    add_completion=False
)
console = Console()


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
    if file_name in significant_extensions: 
        return True
    _, ext = os.path.splitext(file_path)
    # Check also for database files without extension or with different naming
    if is_sqlite_database(file_path):
        return True
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
                # Add database indicator
                full_path = os.path.join(dirpath, f)
                prefix = "🗄️ " if is_sqlite_database(full_path) else "📄 "
                tree_str += f"{sub_indent}{prefix}{f}\n"
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
    """Read file content with special handling for databases."""
    # Handle SQLite databases specially
    if is_sqlite_database(file_path):
        try:
            schema = get_database_schema(file_path)
            return generate_database_context_full(schema, os.path.basename(file_path))
        except Exception as e:
            return f"!!! Error reading database: {e} !!!"
    
    # Normal file reading
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
    
    # Special handling for database table focusing
    # Pattern like "database.db/users" means focus on 'users' table in database.db
    db_table_focus = None
    for pattern in focus_patterns:
        if '.db/' in pattern or '.sqlite/' in pattern:
            parts = pattern.split('/')
            if len(parts) >= 2 and any(ext in parts[0] for ext in ['.db', '.sqlite']):
                db_table_focus = (parts[0], parts[1])
                break
    
    for pattern in focus_patterns:
        clean_pattern = pattern.replace(os.sep, '/')
        if fnmatch.fnmatch(rel_path_fwd, clean_pattern):
            return True
        if clean_pattern in rel_path_fwd:
            return True
    return False


def extract_focused_tables(file_path: str, focus_patterns: List[str]) -> List[str]:
    """
    Extract table names from focus patterns for database files.
    Pattern format: "database.db/table_name" or "*.db/users"
    """
    if not is_sqlite_database(file_path):
        return []
    
    db_name = os.path.basename(file_path)
    focused_tables = []
    
    for pattern in focus_patterns:
        if '/' in pattern:
            db_pattern, table_name = pattern.split('/', 1)
            if fnmatch.fnmatch(db_name, db_pattern):
                focused_tables.append(table_name)
    
    return focused_tables


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


def version_callback(value: bool):
    if value:
        try:
            v = get_package_version("deepbase")
            console.print(f"DeepBase version: [bold cyan]{v}[/bold cyan]")
        except PackageNotFoundError:
            console.print("DeepBase version: [yellow]unknown (editable/dev mode)[/yellow]")
        raise typer.Exit()


@app.command()
def create(
    target: str = typer.Argument(
        None,
        help="The file or directory to scan."
    ),
    
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", 
        callback=version_callback, 
        is_eager=True,
        help="Show the application version and exit."
    ),

    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file."),
    
    verbose: bool = typer.Option(False, "--verbose", "-V", help="Show detailed output."),
    
    include_all: bool = typer.Option(False, "--all", "-a", help="Include full content of ALL files."),
    toon_mode: bool = typer.Option(False, "--toon", "-t", help="Use 'Skeleton' mode for non-focused files."),
    focus: Optional[List[str]] = typer.Option(None, "--focus", "-f", help="Pattern to focus on. For DBs: 'file.db/tablename'"),
    focus_file: Optional[str] = typer.Option(None, "--focus-file", "-ff", help="Path to focus patterns file.")
):
    """
    Analyzes a directory OR a single file.
    Hybrid workflow with Context Skeleton + Focused Content.
    Supports SQLite databases with schema extraction.
    """
    
    if target is None:
        ctx = typer.get_current_context()
        console.print("[red]Error: Missing argument 'TARGET'.[/red]")
        console.print(ctx.get_help())
        raise typer.Exit(code=1)

    if not os.path.exists(target):
        console.print(f"[bold red]Error:[/bold red] Target not found: '{target}'")
        raise typer.Exit(code=1)

    # --- LOGICA FOCUS MERGE ---
    active_focus_patterns = []
    if focus: 
        active_focus_patterns.extend(focus)
    if focus_file:
        file_patterns = load_focus_patterns_from_file(focus_file)
        if file_patterns: 
            active_focus_patterns.extend(file_patterns)
    active_focus_patterns = list(set(active_focus_patterns))

    console.print(f"[bold green]Analyzing '{target}'...[/bold green]")
    
    if toon_mode and active_focus_patterns:
         console.print(f"[yellow]Hybrid Mode active: TOON + Focus on {len(active_focus_patterns)} patterns.[/yellow]")
    elif toon_mode:
        console.print("[yellow]TOON Mode active: Minimalist output.[/yellow]")

    # --- STYLE CONFIGURATION ---
    if toon_mode:
        def fmt_header(title): 
            return f"### {title}\n\n"
        def fmt_file_start(path): 
            # Add database indicator
            is_db = is_sqlite_database(os.path.join(os.path.dirname(target) if os.path.isfile(target) else target, path))
            icon = "🗄️ " if is_db else ""
            return f"> FILE: {icon}{path}\n"
        def fmt_file_end(path):   
            return "\n"
        def fmt_separator():      
            return "" 
    else:
        def fmt_header(title): 
            line = "="*80 
            return f"{line}\n### {title} ###\n{line}\n\n"
        def fmt_file_start(path): 
            is_db = is_sqlite_database(os.path.join(os.path.dirname(target) if os.path.isfile(target) else target, path))
            icon = "🗄️ " if is_db else ""
            return f"--- START OF FILE: {icon}{path} ---\n\n"
        def fmt_file_end(path):   
            return f"\n\n--- END OF FILE: {path} ---\n"
        def fmt_separator():      
            return "-" * 40 + "\n\n"

    try:
        with open(output, "w", encoding="utf-8") as outfile:
            
            # CASE 1: SINGLE FILE
            if os.path.isfile(target):
                filename = os.path.basename(target)
                is_db = is_sqlite_database(target)
                
                if is_db:
                    outfile.write(f"# Database Analysis: {filename}\n\n")
                else:
                    outfile.write(f"# File Structure Analysis: {filename}\n\n")
                
                # Handle databases specially
                if is_db:
                    schema = get_database_schema(target)
                    
                    # Determine mode
                    focused_tables = extract_focused_tables(target, active_focus_patterns)
                    is_focused = bool(focused_tables) or (active_focus_patterns and any(
                        fnmatch.fnmatch(filename, p) or p in filename for p in active_focus_patterns
                    ))
                    
                    if toon_mode and not is_focused:
                        # TOON mode: minimal schema
                        outfile.write(fmt_header("DATABASE SCHEMA (TOON)"))
                        outfile.write(generate_toon_representation(target, ""))
                    elif toon_mode and focused_tables:
                        # Hybrid: TOON + focused tables detailed
                        outfile.write(fmt_header("DATABASE SCHEMA (HYBRID)"))
                        outfile.write(generate_database_focused(target, focused_tables))
                    else:
                        # Full mode or focused
                        outfile.write(fmt_header("DATABASE SCHEMA"))
                        if focused_tables:
                            outfile.write(generate_database_focused(target, focused_tables))
                        else:
                            outfile.write(generate_database_context_full(schema, filename))
                
                else:
                    # Regular file handling
                    content = read_file_content(target)
                    structure = get_document_structure(target, content)
                    outfile.write(fmt_header("DOCUMENT STRUCTURE (Outline)"))
                    outfile.write(structure or "N/A")
                    outfile.write("\n\n")
                    
                    if include_all or toon_mode:
                         section = "SEMANTIC SKELETONS (TOON)" if toon_mode else "FILE CONTENT"
                         outfile.write(fmt_header(section))
                         outfile.write(fmt_file_start(filename))
                         if toon_mode: 
                             outfile.write(generate_toon_representation(target, content))
                         else: 
                             outfile.write(content)
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
                            is_db = is_sqlite_database(fpath)
                            
                            # Check focus
                            is_in_focus = active_focus_patterns and matches_focus(fpath, target, active_focus_patterns)
                            
                            # For databases, also check table-level focus
                            focused_tables = []
                            if is_db:
                                focused_tables = extract_focused_tables(fpath, active_focus_patterns)
                                if focused_tables:
                                    is_in_focus = True
                            
                            should_write_full = include_all or is_in_focus
                            should_write_toon = toon_mode and not should_write_full
                            
                            if not should_write_full and not should_write_toon:
                                progress.update(task, advance=1)
                                continue

                            progress.update(task, advance=1, description=f"[cyan]{rel_path}[/cyan]")
                            
                            # Marker for focused items
                            marker = ""
                            if is_in_focus and toon_mode: 
                                marker = " [FOCUSED - FULL CONTENT]"
                            elif is_db:
                                marker = " [DATABASE]"
                            
                            outfile.write(fmt_file_start(rel_path + marker))
                            
                            if is_db:
                                # Database handling
                                if should_write_full:
                                    if focused_tables:
                                        outfile.write(generate_database_focused(fpath, focused_tables))
                                    else:
                                        schema = get_database_schema(fpath)
                                        outfile.write(generate_database_context_full(schema, os.path.basename(fpath)))
                                else:  # TOON mode
                                    outfile.write(generate_toon_representation(fpath, ""))
                            else:
                                # Regular file handling
                                content = read_file_content(fpath)
                                if should_write_full: 
                                    outfile.write(content)
                                elif should_write_toon: 
                                    outfile.write(generate_toon_representation(fpath, content))
                            
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