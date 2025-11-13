# Project Context: DeepBase

================================================================================
### PROJECT STRUCTURE ###
================================================================================

Project Structure in: /home/follen/Documents/uni-git/DeepBase

📂 ./
    📄 .gitignore
    📄 README.md
    📄 pyproject.toml
    📂 src/
        📂 deepbase/
            📄 __init__.py
            📄 main.py
        📂 deepbase.egg-info/
    📂 examples/
        📄 deepbase_context.md
    📂 tests/
        📄 test_main.py


================================================================================
### FILE CONTENTS ###
================================================================================

--- START OF FILE: .gitignore ---

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
debug.log
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
# According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
# However, in case you generate it automatically, you may want to ignore it.
# Pipfile.lock

# poetry
# According to python-poetry/poetry#519, it is recommended to include poetry.lock in version control.
# This is especially if you are building a library.
# poetry.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env.bak
venv.bak

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# Abstra
# Abstra is an AI-powered process automation framework.
# Ignore directories containing user credentials, local state, and settings.
# Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer, 
#  you could uncomment the following to ignore the entire vscode folder
# .vscode/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
.cursorignore
.cursorindexingignore

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/


--- END OF FILE: .gitignore ---

----------------------------------------

--- START OF FILE: README.md ---

# DeepBase

**DeepBase** is a command-line tool that analyzes a project directory, extracts the folder structure and the content of all significant code files, and consolidates them into a single text/markdown file.

This unified "context" is perfect for providing to a Large Language Model (LLM) to enable it to deeply understand the entire codebase.

## Features

- **Project Structure**: Generates a tree view of the folder and file structure.
- **Smart Filtering**: Automatically ignores common unnecessary directories (e.g., `.git`, `venv`, `node_modules`).
- **Configurable**: Customize ignored directories and included extensions via a `.deepbase.toml` file.
- **Extension Selection**: Includes only files with relevant code or configuration extensions.
- **Unified Output**: Combines everything into a single file, easy to copy and paste.
- **PyPI Ready**: Easy to install via `pip`.

## Installation

You can install DeepBase directly from PyPI:

```sh
pip install deepbase

```

## How to Use

Once installed, you will have the `deepbase` command available in your terminal.

**Basic Usage:**

Navigate to your project folder (or a parent folder) and run:

```sh
deepbase .
```
*The dot `.` indicates the current directory.*

This command will create a file called `llm_context.md` in the current directory.

**Specify Directory and Output File:**

```sh
deepbase /path/to/your/project -o project_context.txt
```

### Advanced Configuration

You can customize DeepBase's behavior by creating a `.deepbase.toml` file in the root of the project you are analyzing.

**Example `.deepbase.toml`:**
```toml
# Add more directories to ignore.
# These will be added to the default ones.
ignore_dirs = [
  "my_assets_folder",
  "experimental"
]

# Add more extensions or filenames to include.
significant_extensions = [
  ".cfg",
  "Makefile"
]
```

## License

This project is released under the GPL 3 license. See the `LICENSE` file for details.

--- END OF FILE: README.md ---

----------------------------------------

--- START OF FILE: pyproject.toml ---

# pyproject.toml

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "deepbase"
# Increment the version to reflect changes
version = "1.2.0" 
authors = [
  { name="Your Name", email="your@email.com" },
]
description = "A CLI utility to consolidate project context for LLMs."
readme = "README.md"
license = { file="LICENSE" }
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development",
    "Topic :: Utilities",
]
keywords = ["llm", "context", "developer-tool", "ai", "code-analysis", "deepbase"]

# Main project dependencies
dependencies = [
    "typer[all]",   # For a modern and robust CLI
    "rich",         # For colored output and progress bars
    "tomli",        # To read .toml configuration files
    "chardet"       # To reliably detect file encoding
]

[project.urls]
"Homepage" = "https://github.com/follen99/deepbase"
"Bug Tracker" = "https://github.com/follen99/deepbase/issues"

# Update the script to point to the Typer app object
[project.scripts]
deepbase = "deepbase.main:app"

# Optional dependencies for development (e.g., testing)
[project.optional-dependencies]
dev = [
    "pytest",
]

--- END OF FILE: pyproject.toml ---

----------------------------------------

--- START OF FILE: src/deepbase/__init__.py ---



--- END OF FILE: src/deepbase/__init__.py ---

----------------------------------------

--- START OF FILE: src/deepbase/main.py ---

# src/deepbase/main.py

import os
import typer
from rich.console import Console
from rich.progress import Progress
import tomli
import chardet
from typing import List, Dict, Any, Set

# --- DEFAULT CONFIGURATION ---

DEFAULT_CONFIG = {
    "ignore_dirs": {
        "__pycache__", ".git", ".idea", ".vscode", "venv", ".venv", "env",
        ".env", "node_modules", "build", "dist", "target", "out", "bin",
        "obj", "logs", "tmp", "eggs", ".eggs", ".pytest_cache", ".tox",
        "site",
    },
    "significant_extensions": {
        ".py", ".java", ".js", ".ts", ".html", ".css", ".scss", ".sql",
        ".md", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat", "Dockerfile",
        ".dockerignore", ".gitignore", "requirements.txt", "pom.xml", "gradlew",
        "pyproject.toml", "setup.py",
    }
}

# --- TOOL INITIALIZATION ---

app = typer.Typer(
    name="deepbase",
    help="Analyzes a project directory and creates a unified context document for an LLM.",
    add_completion=False
)
console = Console()


def load_config(root_dir: str) -> Dict[str, Any]:
    """Loads configuration from .deepbase.toml or uses the default."""
    config_path = os.path.join(root_dir, ".deepbase.toml")
    config = DEFAULT_CONFIG.copy()
    
    if os.path.exists(config_path):
        console.print(f"[bold cyan]Found configuration file: '.deepbase.toml'[/bold cyan]")
        try:
            with open(config_path, "rb") as f:
                user_config = tomli.load(f)
            
            # Merge user config with defaults
            config["ignore_dirs"].update(user_config.get("ignore_dirs", []))
            config["significant_extensions"].update(user_config.get("significant_extensions", []))
            console.print("[green]Custom configuration loaded successfully.[/green]")

        except tomli.TOMLDecodeError as e:
            console.print(f"[bold red]Error parsing .deepbase.toml:[/bold red] {e}")
            console.print("[yellow]Using default configuration.[/yellow]")
    
    return config


def is_significant_file(file_path: str, significant_extensions: Set[str]) -> bool:
    """Checks if a file is significant based on the provided extensions."""
    file_name = os.path.basename(file_path)
    if file_name in significant_extensions:
        return True
    _, ext = os.path.splitext(file_name)
    return ext in significant_extensions


def generate_directory_tree(root_dir: str, config: Dict[str, Any]) -> str:
    """Generates a text representation of the folder structure."""
    tree_str = f"Project Structure in: {os.path.abspath(root_dir)}\n\n"
    ignore_dirs = config["ignore_dirs"]
    significant_exts = config["significant_extensions"]

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        
        tree_str += f"{indent}ðŸ“‚ {os.path.basename(dirpath) or os.path.basename(os.path.abspath(root_dir))}/\n"
        
        sub_indent = ' ' * 4 * (level + 1)
        
        for f in sorted(filenames):
            if is_significant_file(os.path.join(dirpath, f), significant_exts):
                tree_str += f"{sub_indent}ðŸ“„ {f}\n"
    
    return tree_str


def get_all_significant_files(root_dir: str, config: Dict[str, Any]) -> List[str]:
    """Gets a list of all significant files to be included."""
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


@app.command()
def create(
    directory: str = typer.Argument(..., help="The root directory of the project to scan."),
    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file that will contain the context."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output, including ignored files.")
):
    """
    Analyzes a project and creates a unified context file for an LLM.
    """
    if not os.path.isdir(directory):
        console.print(f"[bold red]Error:[/bold red] The specified directory does not exist: '{directory}'")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Starting scan of '{directory}'...[/bold green]")
    
    config = load_config(directory)
    
    try:
        with open(output, "w", encoding="utf-8") as outfile:
            # 1. Write the header
            outfile.write(f"# Project Context: {os.path.basename(os.path.abspath(directory))}\n\n")
            
            # 2. Write the structure
            outfile.write("="*80 + "\n### PROJECT STRUCTURE ###\n" + "="*80 + "\n\n")
            directory_tree = generate_directory_tree(directory, config)
            outfile.write(directory_tree)
            outfile.write("\n\n")

            # 3. Write the file contents
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
                        
                        # Detect encoding
                        detection = chardet.detect(raw_data)
                        encoding = detection['encoding'] if detection['encoding'] else 'utf-8'
                        
                        # Read and write content with robust error handling
                        content = raw_data.decode(encoding, errors="replace")
                        outfile.write(content)

                    except Exception as e:
                        outfile.write(f"!!! Error while reading file: {e} !!!\n")
                    
                    outfile.write(f"\n\n--- END OF FILE: {relative_path} ---\n\n")
                    outfile.write("-" * 40 + "\n\n")
        
        console.print(f"\n[bold green]âœ“ SUCCESS[/bold green]: Context successfully created in file: [cyan]'{output}'[/cyan]")

    except IOError as e:
        console.print(f"\n[bold red]Error writing to output file:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

--- END OF FILE: src/deepbase/main.py ---

----------------------------------------

--- START OF FILE: examples/deepbase_context.md ---

# Project Context: DeepBase

================================================================================
### PROJECT STRUCTURE ###
================================================================================

Project Structure in: /home/follen/Documents/uni-git/DeepBase

ðŸ“‚ ./
    ðŸ“„ .gitignore
    ðŸ“„ README.md
    ðŸ“„ pyproject.toml
    ðŸ“‚ src/
        ðŸ“‚ deepbase/
            ðŸ“„ __init__.py
            ðŸ“„ main.py
        ðŸ“‚ deepbase.egg-info/
    ðŸ“‚ examples/
        ðŸ“„ deepbase_context.md
    ðŸ“‚ tests/
        ðŸ“„ test_main.py


================================================================================
### FILE CONTENTS ###
================================================================================

--- START OF FILE: .gitignore ---

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
debug.log
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
# According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
# However, in case you generate it automatically, you may want to ignore it.
# Pipfile.lock

# poetry
# According to python-poetry/poetry#519, it is recommended to include poetry.lock in version control.
# This is especially if you are building a library.
# poetry.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env.bak
venv.bak

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# Abstra
# Abstra is an AI-powered process automation framework.
# Ignore directories containing user credentials, local state, and settings.
# Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer, 
#  you could uncomment the following to ignore the entire vscode folder
# .vscode/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
.cursorignore
.cursorindexingignore

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/


--- END OF FILE: .gitignore ---

----------------------------------------

--- START OF FILE: README.md ---

# DeepBase

**DeepBase** is a command-line tool that analyzes a project directory, extracts the folder structure and the content of all significant code files, and consolidates them into a single text/markdown file.

This unified "context" is perfect for providing to a Large Language Model (LLM) to enable it to deeply understand the entire codebase.

## Features

- **Project Structure**: Generates a tree view of the folder and file structure.
- **Smart Filtering**: Automatically ignores common unnecessary directories (e.g., `.git`, `venv`, `node_modules`).
- **Configurable**: Customize ignored directories and included extensions via a `.deepbase.toml` file.
- **Extension Selection**: Includes only files with relevant code or configuration extensions.
- **Unified Output**: Combines everything into a single file, easy to copy and paste.
- **PyPI Ready**: Easy to install via `pip`.

## Installation

You can install DeepBase directly from PyPI:

```sh
pip install deepbase

```

## How to Use

Once installed, you will have the `deepbase` command available in your terminal.

**Basic Usage:**

Navigate to your project folder (or a parent folder) and run:

```sh
deepbase .
```
*The dot `.` indicates the current directory.*

This command will create a file called `llm_context.md` in the current directory.

**Specify Directory and Output File:**

```sh
deepbase /path/to/your/project -o project_context.txt
```

### Advanced Configuration

You can customize DeepBase's behavior by creating a `.deepbase.toml` file in the root of the project you are analyzing.

**Example `.deepbase.toml`:**
```toml
# Add more directories to ignore.
# These will be added to the default ones.
ignore_dirs = [
  "my_assets_folder",
  "experimental"
]

# Add more extensions or filenames to include.
significant_extensions = [
  ".cfg",
  "Makefile"
]
```

## License

This project is released under the GPL 3 license. See the `LICENSE` file for details.

--- END OF FILE: README.md ---

----------------------------------------

--- START OF FILE: pyproject.toml ---

# pyproject.toml

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "deepbase"
# Increment the version to reflect changes
version = "1.2.0" 
authors = [
  { name="Your Name", email="your@email.com" },
]
description = "A CLI utility to consolidate project context for LLMs."
readme = "README.md"
license = { file="LICENSE" }
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development",
    "Topic :: Utilities",
]
keywords = ["llm", "context", "developer-tool", "ai", "code-analysis", "deepbase"]

# Main project dependencies
dependencies = [
    "typer[all]",   # For a modern and robust CLI
    "rich",         # For colored output and progress bars
    "tomli",        # To read .toml configuration files
    "chardet"       # To reliably detect file encoding
]

[project.urls]
"Homepage" = "https://github.com/follen99/deepbase"
"Bug Tracker" = "https://github.com/follen99/deepbase/issues"

# Update the script to point to the Typer app object
[project.scripts]
deepbase = "deepbase.main:app"

# Optional dependencies for development (e.g., testing)
[project.optional-dependencies]
dev = [
    "pytest",
]

--- END OF FILE: pyproject.toml ---

----------------------------------------

--- START OF FILE: src/deepbase/__init__.py ---



--- END OF FILE: src/deepbase/__init__.py ---

----------------------------------------

--- START OF FILE: src/deepbase/main.py ---



--- END OF FILE: examples/deepbase_context.md ---

----------------------------------------

--- START OF FILE: tests/test_main.py ---

# tests/test_main.py

import os
from typer.testing import CliRunner
from deepbase.main import app

# Runner instance to execute Typer app commands
runner = CliRunner()

def test_create_context_successfully(tmp_path):
    """
    Tests the creation of a context file in a successful scenario.
    """
    # 1. Create a mock project structure
    project_dir = tmp_path / "my_test_project"
    project_dir.mkdir()
    (project_dir / "main.py").write_text("print('hello world')")
    (project_dir / "README.md").write_text("# My Project")
    
    # Create a directory to ignore
    ignored_dir = project_dir / "venv"
    ignored_dir.mkdir()
    (ignored_dir / "ignored_file.py").write_text("ignore me")
    
    output_file = tmp_path / "context.md"

    # 2. Execute the CLI command with arguments in the correct order
    result = runner.invoke(app, [str(project_dir), "--output", str(output_file)])

    # 3. Verify the results
    assert result.exit_code == 0
    assert "SUCCESS" in result.stdout
    assert output_file.exists()

    content = output_file.read_text()
    
    # Check that significant files are included
    assert "--- START OF FILE: main.py ---" in content
    assert "print('hello world')" in content
    assert "--- START OF FILE: README.md ---" in content
    
    # Check that ignored directory and files are not present
    assert "venv" not in content
    assert "ignored_file.py" not in content

def test_directory_not_found():
    """
    Tests the behavior when the input directory does not exist.
    """
    result = runner.invoke(app, ["non_existent_dir"])
    assert result.exit_code == 1
    assert "directory does not exist" in result.stdout

--- END OF FILE: tests/test_main.py ---

----------------------------------------

