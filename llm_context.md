# Project Context: DeepBase

================================================================================
### PROJECT STRUCTURE ###
================================================================================

> Total Size: 93.03 KB | Est. Tokens: ~23,817
📁 DeepBase/
├── 📄 .gitignore (3.4% | ~805t)
├── 📄 CHANGELOG.md (1.1% | ~255t)
├── 📄 README.md (3.8% | ~908t)
├── 📁 docs/ (2.1% | ~500t)
│   ├── 📄 index.md (2.0% | ~487t)
│   └── 📄 reference.md (0.1% | ~13t)
├── 📁 examples/ (26.2% | ~6.2k t)
│   └── 📄 deepbase_context.md (26.2% | ~6.2k t)
├── 📄 mkdocs.yml (1.0% | ~227t)
├── 📄 pyproject.toml (1.5% | ~363t)
├── 📁 src/ (52.0% | ~12.4k t)
│   ├── 📁 deepbase/ (52.0% | ~12.4k t)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 database.py (9.1% | ~2.2k t)
│   │   ├── 📄 main.py (24.4% | ~5.8k t)
│   │   ├── 📁 parsers/ (12.5% | ~3.0k t)
│   │   │   ├── 📄 __init__.py (0.2% | ~53t)
│   │   │   ├── 📄 document.py (2.0% | ~485t)
│   │   │   ├── 📄 fallback.py (0.9% | ~226t)
│   │   │   ├── 📄 interface.py (0.4% | ~96t)
│   │   │   ├── 📄 python.py (6.9% | ~1.6k t)
│   │   │   └── 📄 registry.py (2.0% | ~477t)
│   │   └── 📄 toon.py (6.1% | ~1.4k t)
│   └── 📁 deepbase.egg-info/
└── 📁 tests/ (9.0% | ~2.1k t)
    ├── 📁 database/
    └── 📄 test_suite_python.py (9.0% | ~2.1k t)


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

--- START OF FILE: CHANGELOG.md ---

## [1.7.0] - 2024-02-12

### Added
- **Smart Token Estimation**: Added approximate token count (~4 chars/token) and file size percentage next to every file and folder in the tree view.
- **Recursive Directory Stats**: Parent folders now show the cumulative size and token count of their contents.
- **Enhanced Tree Visualization**: Replaced simple indentation with proper ASCII tree branches (`├──`, `└──`, `│`) for better readability.
- **CLI Links**: Added links to Documentation, Repository, and Issues in the `--help` output.

### Changed
- **React/JS Optimization**: Automatically ignores `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, and mobile build folders (`ios/`, `android/`) to save tokens.
- **Self-Exclusion Logic**: DeepBase now strictly ignores any existing file named `llm_context.md` (or the specified output name) in the target directory to prevent data duplication.

### Fixed
- Fixed an issue where previous context files were included in the analysis, doubling the token count.

--- END OF FILE: CHANGELOG.md ---
----------------------------------------

--- START OF FILE: README.md ---

# DeepBase

**DeepBase** is a command-line tool that analyzes a project directory, extracts the folder structure and the content of all significant code files, and consolidates them into a single text/markdown file.

This unified "context" is perfect for providing to a Large Language Model (LLM) to enable it to deeply understand the entire codebase.

## Features

- **Project Structure**: Generates a tree view of the folder and file structure.
- **Smart Filtering**: Automatically ignores common unnecessary directories (e.g., `.git`, `venv`, `node_modules`).
- **Token Optimization (TOON)**: Capable of generating "Semantic Skeletons" (class definitions, function signatures, docstrings) instead of full code to save up to 90% of tokens.
- **Hybrid Focus Mode**: Combine lightweight context for the whole project with full content only for specific files or folders.
- **Configurable**: Customize ignored directories and included extensions via a `.deepbase.toml` file.
- **Unified Output**: Combines everything into a single file, easy to copy and paste.
- **PyPI Ready**: Easy to install via `pip`.

## Installation

You can install DeepBase directly from PyPI:

```sh
pip install deepbase
```

## How to Use

Once installed, use the `deepbase` command followed by the target (directory or file).

### 1. Basic Project Analysis

**Structure Only (Default)**
Quickly generate a tree view of your project folders and files. No code content is included.

```sh
deepbase .
```

**Include All Content**
To generate the full context including the code of all significant files, use the `--all` (or `-a`) flag.
*Warning: use this only for small projects.*

```sh
deepbase . --all
```

### 2. Smart Token Optimization (TOON)

For large projects, sending all code to an LLM is expensive and inefficient. **TOON (Token Oriented Object Notation)** extracts only the semantic "skeleton" of your code (classes, signatures, docstrings), ignoring implementations.

```sh
deepbase . --toon
# or
deepbase . -t
```
*Result: LLMs understand your architecture using minimal tokens.*

### 3. Hybrid Mode (Focus)

This is the power user feature. You can provide the TOON skeleton for the entire project (background context) while focusing on specific files (full content).

**Focus via CLI:**
Use `-f` or `--focus` with glob patterns (e.g., `*auth*`, `src/utils/*`).

```sh
deepbase . --toon --focus "server/controllers/*" --focus "client/src/login.js"
```

**Focus via File:**
Instead of typing patterns every time, create a text file (e.g., `context_task.txt`) with the list of files/folders you are working on.

*content of `context_task.txt`:*
```text
server/routes/auth.js
server/models/User.js
client/src/components/LoginForm.jsx
```

Run deepbase loading the file:
```sh
deepbase . --toon --focus-file context_task.txt
```

### 4. Single File Analysis

DeepBase supports analyzing a single specific file.

**Structure Only (Default)**
Extracts only the outline/headers. Useful for large documentation files.

```sh
deepbase README.md
```

**Structure + Content**
Appends the full content after the structure.

```sh
deepbase README.md --all
```

### Configuration (.deepbase.toml)

You can customize behavior by creating a `.deepbase.toml` file in your project root:

```toml
ignore_dirs = ["my_assets", "experimental"]
significant_extensions = [".cfg", "Makefile", ".tsx"]
```

## Development Workflow

If you want to contribute or test the tool locally:

```sh
# Install in editable mode
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is released under the GPL 3 license. See the `LICENSE` file for details.
```

--- END OF FILE: README.md ---
----------------------------------------

--- START OF FILE: mkdocs.yml ---

site_name: DeepBase
site_description: A CLI tool to consolidate project context for LLMs.
site_url: https://follen99.github.io/deepbase/  # Aggiorna con il tuo username
repo_url: https://github.com/follen99/deepbase
repo_name: follen99/deepbase

theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: teal
      accent: purple
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - scheme: slate
      primary: teal
      accent: lime
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - content.code.copy
    - navigation.expand
    - navigation.top
    - search.suggest

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [src]  # Dice al plugin dove trovare il codice sorgente

nav:
  - Home: index.md
  - API Reference: reference.md

--- END OF FILE: mkdocs.yml ---
----------------------------------------

--- START OF FILE: pyproject.toml ---

# pyproject.toml

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "deepbase"
# Increment the version to reflect changes
version = "1.8.0" 
authors = [
  { name="Giuliano Ranauro", email="ranaurogln@email.com" },
]
description = "A CLI utility to consolidate project context for LLMs."
readme = "README.md"
license = { file="LICENSE" }
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
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

docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.24.0",
]

--- END OF FILE: pyproject.toml ---
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
        
        tree_str += f"{indent}Ã°Å¸â€œâ€š {os.path.basename(dirpath) or os.path.basename(os.path.abspath(root_dir))}/\n"
        
        sub_indent = ' ' * 4 * (level + 1)
        
        for f in sorted(filenames):
            if is_significant_file(os.path.join(dirpath, f), significant_exts):
                tree_str += f"{sub_indent}Ã°Å¸â€œâ€ž {f}\n"
    
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
        
        console.print(f"\n[bold green]Ã¢Å“â€œ SUCCESS[/bold green]: Context successfully created in file: [cyan]'{output}'[/cyan]")

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

Ã°Å¸â€œâ€š ./
    Ã°Å¸â€œâ€ž .gitignore
    Ã°Å¸â€œâ€ž README.md
    Ã°Å¸â€œâ€ž pyproject.toml
    Ã°Å¸â€œâ€š src/
        Ã°Å¸â€œâ€š deepbase/
            Ã°Å¸â€œâ€ž __init__.py
            Ã°Å¸â€œâ€ž main.py
        Ã°Å¸â€œâ€š deepbase.egg-info/
    Ã°Å¸â€œâ€š examples/
        Ã°Å¸â€œâ€ž deepbase_context.md
    Ã°Å¸â€œâ€š tests/
        Ã°Å¸â€œâ€ž test_main.py


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



--- END OF FILE: examples/deepbase_context.md ---
----------------------------------------

--- START OF FILE: tests/test_suite_python.py ---

# tests/test_suite_python.py

import os
import typer
from typer.testing import CliRunner
from deepbase.main import main
import sqlite3

# Creiamo un'app Typer temporanea per il testing
test_app = typer.Typer()
test_app.command()(main)

runner = CliRunner()

class TestPythonSuite:
    """
    Test suite dedicata all'analisi di progetti Python con DeepBase.
    FIX: Specifica sempre l'output path esplicito per evitare FileNotFoundError.
    FIX: Controlla il contenuto del file generato, non lo stdout, per la struttura.
    """

    def create_dummy_python_project(self, root):
        """Helper per popolare una directory con file Python finti."""
        # 1. File principale
        main_py = root / "main.py"
        main_py.write_text("""
import os

def hello_world():
    print("Hello content")
    return True

class MyClass:
    def method_one(self):
        # This is a comment inside
        return 1
""", encoding="utf-8")

        # 2. Modulo utils
        utils_dir = root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def help_me():\n    pass", encoding="utf-8")

        # 3. File da ignorare (segreto)
        (root / "secrets.py").write_text("API_KEY = '123'", encoding="utf-8")

        # 4. Cartella da ignorare (es. cache)
        cache_dir = root / ".mypy_cache"
        cache_dir.mkdir()
        (cache_dir / "data.json").write_text("{}", encoding="utf-8")

    def test_basic_structure(self, tmp_path):
        """Testa che il comando base generi la struttura nel file."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        
        # Passiamo esplicitamente l'output file nel tmp_path
        result = runner.invoke(test_app, [str(tmp_path), "-o", str(output_file)])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica presenza nell'albero (DENTRO IL FILE, non nello stdout)
        assert "main.py" in content
        assert "utils/" in content
        
        # Verifica che il CONTENUTO del codice NON ci sia
        assert "def hello_world" not in content
        assert "import os" not in content

    def test_flag_all_content(self, tmp_path):
        """Testa --all: deve includere tutto il codice."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--all", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # Deve contenere il corpo delle funzioni
        assert "print(\"Hello content\")" in content
        assert "class MyClass:" in content

    def test_flag_light_mode(self, tmp_path):
        """Testa --light: deve includere firme ma NON il corpo."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # Deve contenere la notice Light Mode
        assert "[LIGHT MODE]" in content
        
        # Deve contenere le firme (via AST parsing)
        # Nota: controlliamo stringhe parziali per evitare problemi di formattazione spazi
        assert "def hello_world" in content
        assert "class MyClass:" in content
        
        # NON deve contenere il corpo del codice
        assert "print(\"Hello content\")" not in content
        assert "return 1" not in content

    def test_focus_mode_hybrid(self, tmp_path):
        """Testa --focus combined (ibrido)."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        # Focus solo su main.py
        result = runner.invoke(test_app, [str(tmp_path), "--focus", "main.py", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # main.py deve essere FULL
        assert "--- START OF FILE: main.py ---" in content
        assert "print(\"Hello content\")" in content
        
        # utils/helper.py NON era in focus, quindi non dovrebbe esserci il contenuto
        assert "--- START OF FILE: utils/helper.py ---" not in content

    def test_focus_with_light_background(self, tmp_path):
        """Testa --light insieme a --focus."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        # Focus su main.py, ma background --light
        result = runner.invoke(test_app, [str(tmp_path), "--light", "--focus", "main.py", "-o", str(output_file)])
        
        content = output_file.read_text(encoding="utf-8")
        
        # main.py FULL
        assert "print(\"Hello content\")" in content
        
        # utils/helper.py LIGHT (deve esserci la firma)
        assert "def help_me" in content

    def test_toml_configuration(self, tmp_path):
        """Testa che .deepbase.toml venga letto e rispettato."""
        self.create_dummy_python_project(tmp_path)
        
        # Crea configurazione per ignorare "secrets.py"
        toml_file = tmp_path / ".deepbase.toml"
        toml_file.write_text('ignore_files = ["secrets.py"]', encoding="utf-8")
        
        output_file = tmp_path / "llm_context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--all", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # secrets.py NON deve apparire
        assert "secrets.py" not in content
        assert "API_KEY" not in content

    def test_custom_output_path(self, tmp_path):
        """Testa l'opzione -o per il file di output."""
        self.create_dummy_python_project(tmp_path)
        
        custom_out = tmp_path / "custom_analysis.txt"
        result = runner.invoke(test_app, [str(tmp_path), "-o", str(custom_out)])
        
        assert result.exit_code == 0
        assert custom_out.exists()
        
    def test_error_handling_invalid_path(self):
        """Testa che il programma gestisca percorsi inesistenti."""
        result = runner.invoke(test_app, ["/percorso/inesistente/assoluto"])
        assert result.exit_code == 1
        assert "Target not found" in result.stdout
        
    def test_database_handling(self, tmp_path):
        """Testa il supporto per database SQLite (schema extraction e light mode)."""
        import sqlite3  # Import necessario qui o in cima al file

        # Creiamo una cartella e un DB reale
        project_dir = tmp_path / "db_project"
        project_dir.mkdir()
        db_path = project_dir / "test_db.sqlite"

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL)")
        cursor.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT)")
        conn.commit()
        conn.close()

        output_file = project_dir / "context.md"

        # 1. Test Full Mode (--all) -> Deve mostrare schema dettagliato
        result = runner.invoke(test_app, [str(project_dir), "--all", "-o", str(output_file)])
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")

        # Verifica che il DB sia stato processato
        assert "test_db.sqlite" in content
        
        # Verifica il contenuto generato da generate_database_context_full
        # Nota: "DATABASE SCHEMA" appare solo in single-file mode, qui cerchiamo il contenuto reale
        assert "Table: `users`" in content
        # Verifica parziale di una colonna per assicurarsi che lo schema sia stato letto
        assert "username" in content
        assert "TEXT" in content

        # 2. Test Light Mode (--light) -> Deve mostrare schema compatto (TOON)
        result = runner.invoke(test_app, [str(project_dir), "--light", "-o", str(output_file)])
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica firma compatta (TOON)
        # Cerca la definizione della tabella users e la colonna id
        assert "users" in content
        # Verifica formato TOON: nome:tipo
        assert "id:INTEGER" in content

--- END OF FILE: tests/test_suite_python.py ---
----------------------------------------

--- START OF FILE: src/deepbase/__init__.py ---



--- END OF FILE: src/deepbase/__init__.py ---
----------------------------------------

--- START OF FILE: src/deepbase/database.py ---

# src/deepbase/database.py
"""
Database context extraction module for DeepBase.
Handles SQLite databases to provide structured context about schema and tables.
"""

import sqlite3
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ColumnInfo:
    name: str
    data_type: str
    nullable: bool
    default: Optional[str]
    primary_key: bool


@dataclass
class TableInfo:
    name: str
    columns: List[ColumnInfo]
    foreign_keys: List[Dict[str, str]]
    indexes: List[Dict[str, Any]]
    row_count: int


@dataclass
class DatabaseSchema:
    tables: List[TableInfo]
    total_size_bytes: int
    total_tables: int
    total_rows: int


def get_database_schema(db_path: str) -> DatabaseSchema:
    """
    Extract complete schema information from SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get database size
    total_size = os.path.getsize(db_path)
    
    # Get all tables (excluding sqlite internal tables)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    table_names = [row[0] for row in cursor.fetchall()]
    
    tables = []
    total_rows = 0
    
    for table_name in table_names:
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        row_count = cursor.fetchone()[0]
        total_rows += row_count
        
        # Get column info using PRAGMA
        cursor.execute(f"PRAGMA table_info(`{table_name}`)")
        columns = []
        for row in cursor.fetchall():
            col = ColumnInfo(
                name=row[1],
                data_type=row[2],
                nullable=not row[3],  # notnull column: 0=true, 1=false
                default=row[4],
                primary_key=bool(row[5])
            )
            columns.append(col)
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list(`{table_name}`)")
        foreign_keys = []
        for row in cursor.fetchall():
            fk = {
                "id": row[0],
                "seq": row[1],
                "table": row[2],
                "from": row[3],
                "to": row[4],
                "on_update": row[5],
                "on_delete": row[6]
            }
            foreign_keys.append(fk)
        
        # Get indexes
        cursor.execute(f"PRAGMA index_list(`{table_name}`)")
        indexes = []
        for row in cursor.fetchall():
            index_name = row[1]
            cursor.execute(f"PRAGMA index_info(`{index_name}`)")
            index_columns = [r[2] for r in cursor.fetchall()]
            indexes.append({
                "name": index_name,
                "unique": row[2],
                "columns": index_columns
            })
        
        table_info = TableInfo(
            name=table_name,
            columns=columns,
            foreign_keys=foreign_keys,
            indexes=indexes,
            row_count=row_count
        )
        tables.append(table_info)
    
    conn.close()
    
    return DatabaseSchema(
        tables=tables,
        total_size_bytes=total_size,
        total_tables=len(tables),
        total_rows=total_rows
    )


def generate_database_context_full(schema: DatabaseSchema, db_name: str) -> str:
    """
    Generate full detailed context for --all mode.
    Includes complete schema, relationships, and sample data hints.
    """
    lines = [
        f"# Database: {db_name}",
        f"## Overview",
        f"- Total Tables: {schema.total_tables}",
        f"- Total Rows: {schema.total_rows:,}",
        f"- File Size: {schema.total_size_bytes:,} bytes ({schema.total_size_bytes / 1024:.2f} KB)",
        "",
        "## Schema Details",
        ""
    ]
    
    for table in schema.tables:
        lines.extend([
            f"### Table: `{table.name}`",
            f"- Rows: {table.row_count:,}",
            ""
        ])
        
        # Columns
        lines.append("#### Columns:")
        lines.append("| Column | Type | Nullable | Default | PK |")
        lines.append("|--------|------|----------|---------|-----|")
        for col in table.columns:
            pk_mark = "✓" if col.primary_key else ""
            null_mark = "✓" if col.nullable else "NOT NULL"
            default_val = col.default if col.default else "-"
            lines.append(f"| `{col.name}` | {col.data_type} | {null_mark} | {default_val} | {pk_mark} |")
        lines.append("")
        
        # Foreign Keys
        if table.foreign_keys:
            lines.append("#### Foreign Keys:")
            for fk in table.foreign_keys:
                lines.append(f"- `{fk['from']}` → `{fk['table']}`.`{fk['to']}` (ON UPDATE: {fk['on_update']}, ON DELETE: {fk['on_delete']})")
            lines.append("")
        
        # Indexes
        if table.indexes:
            lines.append("#### Indexes:")
            for idx in table.indexes:
                unique_str = "UNIQUE " if idx['unique'] else ""
                lines.append(f"- {unique_str}`{idx['name']}` on ({', '.join(f'`{c}`' for c in idx['columns'])})")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def generate_database_context_toon(schema: DatabaseSchema, db_name: str) -> str:
    """
    Generate minimal TOON-style context (skeleton only).
    Best for large databases where token efficiency matters.
    """
    lines = [
        f"DB: {db_name}",
        f"Tables: {schema.total_tables} | Rows: {schema.total_rows:,}",
        ""
    ]
    
    for table in schema.tables:
        # Compact representation: Table(columns) [FKs]
        col_defs = []
        for col in table.columns:
            flags = []
            if col.primary_key:
                flags.append("PK")
            if not col.nullable:
                flags.append("NN")
            flag_str = f"[{','.join(flags)}]" if flags else ""
            col_defs.append(f"{col.name}:{col.data_type}{flag_str}")
        
        fk_refs = []
        for fk in table.foreign_keys:
            fk_refs.append(f"{fk['from']}→{fk['table']}.{fk['to']}")
        
        fk_str = f" | FK: {', '.join(fk_refs)}" if fk_refs else ""
        lines.append(f"T: {table.name}({', '.join(col_defs)}){fk_str}")
    
    return "\n".join(lines)


def generate_database_context_hybrid(schema: DatabaseSchema, db_name: str, focused_tables: List[str]) -> str:
    """
    Generate hybrid context: TOON for all, full detail for focused tables.
    """
    lines = [
        f"# Database: {db_name}",
        f"## Overview",
        f"- Total Tables: {schema.total_tables}",
        f"- Total Rows: {schema.total_rows:,}",
        "",
        "## Schema (TOON + Focus)",
        ""
    ]
    
    for table in schema.tables:
        is_focused = table.name in focused_tables or any(f in table.name for f in focused_tables)
        
        if is_focused:
            # Full detail for focused tables
            lines.extend([
                f"### [FOCUSED] Table: `{table.name}` ⭐",
                f"- Rows: {table.row_count:,}",
                ""
            ])
            
            lines.append("#### Columns:")
            lines.append("| Column | Type | Nullable | Default | PK |")
            lines.append("|--------|------|----------|---------|-----|")
            for col in table.columns:
                pk_mark = "✓" if col.primary_key else ""
                null_mark = "✓" if col.nullable else "NOT NULL"
                default_val = col.default if col.default else "-"
                lines.append(f"| `{col.name}` | {col.data_type} | {null_mark} | {default_val} | {pk_mark} |")
            lines.append("")
            
            if table.foreign_keys:
                lines.append("#### Foreign Keys:")
                for fk in table.foreign_keys:
                    lines.append(f"- `{fk['from']}` → `{fk['table']}`.`{fk['to']}`")
                lines.append("")
        else:
            # TOON style for non-focused
            col_names = [f"{col.name}:{col.data_type}" + ("(PK)" if col.primary_key else "") 
                        for col in table.columns]
            lines.append(f"- `{table.name}`: {', '.join(col_names)}")
    
    return "\n".join(lines)


def is_sqlite_database(file_path: str) -> bool:
    """
    Check if file is a valid SQLite database by reading magic bytes.
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(16)
            return header[:16] == b'SQLite format 3\x00'
    except:
        return False

--- END OF FILE: src/deepbase/database.py ---
----------------------------------------

--- START OF FILE: src/deepbase/main.py ---

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

from deepbase.toon import generate_toon_representation, generate_light_representation, generate_database_focused
from deepbase.parsers import get_document_structure
from deepbase.database import is_sqlite_database, get_database_schema, generate_database_context_full

from rich.table import Table
from rich.panel import Panel

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

LIGHT_MODE_NOTICE = """> **[LIGHT MODE]** Questo file √® stato generato in modalit√† risparmio token: vengono incluse solo le firme dei metodi/funzioni e i commenti iniziali dei file. Il corpo del codice √® omesso. Se hai bisogno di approfondire un file, una classe o un metodo specifico, chiedi all'utente di fornire la porzione di codice completa.
"""

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


def estimate_tokens_for_content(text: str) -> int:
    return math.ceil(len(text.encode("utf-8")) / 4)

def calculate_light_tokens(file_path: str, content: str) -> int:
    from deepbase.toon import generate_light_representation
    light_repr = generate_light_representation(file_path, content)
    return estimate_tokens_for_content(light_repr)

def is_significant_file(file_path: str, config: Dict[str, Any], output_file_abs: str = None) -> bool:
    file_name = os.path.basename(file_path)

    if output_file_abs and os.path.abspath(file_path) == output_file_abs:
        return False

    if output_file_abs and file_name == os.path.basename(output_file_abs):
        return False

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


def calculate_project_stats(root_dir: str, config: Dict[str, Any], output_file_abs: str, light_mode: bool = False) -> int:
    total_size = 0
    ignore_dirs = config["ignore_dirs"]
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        for f in filenames:
            fpath = os.path.join(dirpath, f)
            if is_significant_file(fpath, config, output_file_abs):
                try:
                    if light_mode and not is_sqlite_database(fpath):
                        content = read_file_content(fpath)
                        light_repr = generate_light_representation(fpath, content)
                        total_size += len(light_repr.encode("utf-8"))
                    else:
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
    output_file_abs: str,
    light_mode: bool = False
) -> Tuple[str, int]:
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
        connector = "‚îî‚îÄ‚îÄ " if is_last else "‚îú‚îÄ‚îÄ "

        if is_dir:
            extension = "    " if is_last else "‚îÇ   "
            sub_tree_str, sub_dir_size = _generate_tree_recursive(
                full_path,
                prefix + extension,
                config,
                total_project_size,
                output_file_abs
            )

            subtree_size += sub_dir_size

            folder_stats = ""
            if total_project_size > 0 and sub_dir_size > 0:
                percent = (sub_dir_size / total_project_size) * 100
                token_est = estimate_tokens(sub_dir_size)
                folder_stats = f" ({percent:.1f}% | {token_est})"

            output_str += f"{prefix}{connector}üìÅ {name}/{folder_stats}\n"
            output_str += sub_tree_str

        else:
            icon = "üóÑÔ∏è " if is_sqlite_database(full_path) else "üìÑ "
            try:
                raw_size = os.path.getsize(full_path)
                if light_mode and not is_sqlite_database(full_path):
                    content = read_file_content(full_path)
                    light_repr = generate_light_representation(full_path, content)
                    size = len(light_repr.encode("utf-8"))
                else:
                    size = raw_size
                subtree_size += size

                # [FIX] Ripristinate le righe mancanti per stampare il file nell'albero!
                file_stats = ""
                if total_project_size > 0 and size > 0:
                    percent = (size / total_project_size) * 100
                    token_est = estimate_tokens(size)
                    file_stats = f" ({percent:.1f}% | {token_est})"

                output_str += f"{prefix}{connector}{icon}{name}{file_stats}\n"

            except OSError:
                pass

    return output_str, subtree_size


def generate_directory_tree(root_dir: str, config: Dict[str, Any], output_file_abs: str, light_mode: bool = False) -> Tuple[str, int, int]:
    abs_root = os.path.abspath(root_dir)
    total_size = calculate_project_stats(root_dir, config, output_file_abs, light_mode)
    tree_body, _ = _generate_tree_recursive(root_dir, "", config, total_size, output_file_abs, light_mode)
    header = f"üìÅ {os.path.basename(abs_root) or '.'}/\n"
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


# --- LOGICA PRINCIPALE (SENZA CLASSE TYPER) ---

def main(
    target: str = typer.Argument(None, help="The file or directory to scan."),
    help: bool = typer.Option(False, "--help", "-h", is_eager=True, help="Show this help message and exit."),
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit."),
    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file."),
    verbose: bool = typer.Option(False, "--verbose", "-V", help="Show detailed output."),
    include_all: bool = typer.Option(False, "--all", "-a", help="Include full content of ALL files."),
    light_mode: bool = typer.Option(False, "--light", "-l", help="Token-saving mode (signatures only)."),
    focus: Optional[List[str]] = typer.Option(None, "--focus", "-f", help="Pattern to focus on (repeatable)."),
    focus_file: Optional[str] = typer.Option(None, "--focus-file", "-ff", help="Path to focus patterns file.")
):
    """
    Analyzes a directory OR a single file.
    Default: structure tree only.
    """
    # 1. Custom HELP Logic
    if help or target is None:
        console.print(Panel.fit(
            "[bold cyan]DeepBase[/bold cyan] ‚Äî Consolidate project context for LLMs\n\n"
            "[bold]Usage:[/bold] [green]deepbase[/green] [OPTIONS] [TARGET]\n\n"
            "[bold]Arguments:[/bold]\n"
            "  [cyan]TARGET[/cyan]  The file or directory to scan  [dim][default: current dir][/dim]\n",
            title="DeepBase v1.7.0", border_style="cyan"
        ))
        
        # Options Table
        options_table = Table(show_header=False, box=None, padding=(0, 2))
        options_table.add_column(style="cyan", no_wrap=True)
        options_table.add_column(style="green", no_wrap=True)
        options_table.add_column()
        
        options = [
            ("-v, --version", "", "Show version and exit"),
            ("-o, --output", "TEXT", "Output file [dim][default: llm_context.md][/dim]"),
            ("-V, --verbose", "", "Show detailed output"),
            ("-a, --all", "", "Include full content of ALL files"),
            ("-l, --light", "", "Token-saving mode (signatures only)"),
            ("-f, --focus", "TEXT", "Pattern to focus on (repeatable)"),
            ("-ff, --focus-file", "TEXT", "Path to focus patterns file"),
            ("-h, --help", "", "Show this message and exit"),
        ]
        for opt, meta, desc in options:
            options_table.add_row(opt, meta, desc)
        
        console.print(Panel(options_table, title="Options", border_style="green", title_align="left"))
        
        config_content = """Create a [cyan].deepbase.toml[/cyan] in your project root:

[dim]# Ignore additional directories[/dim]
[yellow]ignore_dirs = ["my_assets", "experimental"][/yellow]

[dim]# Ignore specific files[/dim]
[yellow]ignore_files = ["*.log", "secrets.env"][/yellow]

[dim]# Add extra file extensions[/dim]
[yellow]significant_extensions = [".cfg", "Makefile", ".tsx"][/yellow]"""

        console.print(Panel(
            config_content,
            title="Configuration (.deepbase.toml)", 
            border_style="yellow",
            title_align="left"
        ))
        
        links_table = Table(show_header=False, box=None, padding=(0, 2))
        links_table.add_column(style="bold")
        links_table.add_column(style="blue")
        
        links_table.add_row("Documentation:", "https://follen99.github.io/DeepBase/")
        links_table.add_row("Repository:", "https://github.com/follen99/DeepBase")
        links_table.add_row("Issues:", "https://github.com/follen99/DeepBase/issues")
        links_table.add_row("PyPI:", "https://pypi.org/project/deepbase/")
        
        console.print(Panel(links_table, title="Links", border_style="blue", title_align="left"))
        
        raise typer.Exit()

    # 2. Main Logic Start
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

    mode_label = ""
    if light_mode:
        mode_label = " [bold yellow](LIGHT ‚Äî signatures only)[/bold yellow]"
    elif include_all:
        mode_label = " [bold cyan](ALL ‚Äî full content)[/bold cyan]"

    console.print(f"[bold green]Analyzing '{target}'...[/bold green]{mode_label}")

    if light_mode:
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
            # CASO 1: Singolo file
            if os.path.isfile(target):
                filename = os.path.basename(target)
                is_db = is_sqlite_database(target)
                outfile.write(f"# Analysis: {filename}\n\n")
                if light_mode:
                    outfile.write(LIGHT_MODE_NOTICE + "\n")

                if is_db:
                    schema = get_database_schema(target)
                    focused_tables = extract_focused_tables(target, active_focus_patterns)
                    is_focused = bool(focused_tables) or (active_focus_patterns and any(
                        fnmatch.fnmatch(filename, p) or p in filename for p in active_focus_patterns
                    ))
                    outfile.write(fmt_header("DATABASE SCHEMA"))
                    if light_mode and not is_focused:
                        outfile.write(generate_light_representation(target, ""))
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
                    if light_mode:
                        outfile.write(generate_light_representation(target, content))
                    else:
                        outfile.write(content)
                    outfile.write(fmt_file_end(filename))

            # CASO 2: Directory
            elif os.path.isdir(target):
                config = load_config(target)
                outfile.write(f"# Project Context: {os.path.basename(os.path.abspath(target))}\n\n")
                if light_mode:
                    outfile.write(LIGHT_MODE_NOTICE + "\n")
                outfile.write(fmt_header("PROJECT STRUCTURE"))

                tree_str, total_bytes, total_tokens = generate_directory_tree(target, config, abs_output_path, light_mode=light_mode)
                
                if light_mode:
                    outfile.write(f"> Total Size (raw): {total_bytes/1024:.2f} KB | Est. Tokens (light): ~{total_tokens:,}\n")
                else:
                    outfile.write(f"> Total Size: {total_bytes/1024:.2f} KB | Est. Tokens: ~{total_tokens:,}\n")
                
                outfile.write(tree_str)
                outfile.write("\n\n")

                if include_all or light_mode or active_focus_patterns:
                    section_title = "FILE CONTENTS"
                    if light_mode: section_title += " (LIGHT ‚Äî signatures only)"
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
                            should_write_light = light_mode and not should_write_full

                            if not should_write_full and not should_write_light:
                                progress.update(task, advance=1)
                                continue

                            progress.update(task, advance=1, description=f"[cyan]{rel_path}[/cyan]")
                            marker = " [FOCUSED]" if (is_in_focus and light_mode) else ""
                            icon = "üóÑÔ∏è " if is_db else ""
                            outfile.write(fmt_file_start(rel_path + marker, icon))

                            if is_db:
                                if should_write_full:
                                    if focused_tables:
                                        outfile.write(generate_database_focused(fpath, focused_tables))
                                    else:
                                        schema = get_database_schema(fpath)
                                        outfile.write(generate_database_context_full(schema, os.path.basename(fpath)))
                                else:
                                    outfile.write(generate_light_representation(fpath, ""))
                            else:
                                content = read_file_content(fpath)
                                if should_write_full:
                                    outfile.write(content)
                                elif should_write_light:
                                    light_output = generate_light_representation(fpath, content)
                                    outfile.write(light_output)

                            outfile.write(fmt_file_end(rel_path))
                            outfile.write(fmt_separator())
                else:
                    console.print("[dim]Directory tree generated. Use --light, --all, or --focus for content.[/dim]")

        console.print(f"\n[bold green]‚úî SUCCESS[/bold green]: Context created in [cyan]'{output}'[/cyan]")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

# Entry point che usa typer.run per gestire il comando come SINGOLO
def app():
    typer.run(main)

if __name__ == "__main__":
    app()

--- END OF FILE: src/deepbase/main.py ---
----------------------------------------

--- START OF FILE: src/deepbase/toon.py ---

# src/deepbase/toon.py

import os
import ast
import json
import re

# Import database handling
from deepbase.database import (
    get_database_schema,
    generate_database_context_toon,
    generate_database_context_hybrid,
    is_sqlite_database
)

# Import new parser registry
from deepbase.parsers.registry import registry

# Manteniamo ToonVisitor originale per la retrocompatibilità (se usato altrove)
# o per la funzione generate_toon_representation "standard" (non light).
class ToonVisitor(ast.NodeVisitor):
    def __init__(self):
        self.output = []
        self.indent_level = 0

    def _log(self, text):
        indent = "  " * self.indent_level
        self.output.append(f"{indent}{text}")

    def visit_ClassDef(self, node):
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        base_str = f"({', '.join(bases)})" if bases else ""
        self._log(f"C: {node.name}{base_str}")

        self.indent_level += 1
        docstring = ast.get_docstring(node)
        if docstring:
            short_doc = docstring.split('\n')[0].strip()
            self._log(f"\"\"\"{short_doc}...\"\"\"")

        self.generic_visit(node)
        self.indent_level -= 1

    def visit_FunctionDef(self, node):
        self._handle_function(node)

    def visit_AsyncFunctionDef(self, node):
        self._handle_function(node, is_async=True)

    def _handle_function(self, node, is_async=False):
        args = [arg.arg for arg in node.args.args]
        args_str = ", ".join(args)
        prefix = "async " if is_async else ""
        self._log(f"{prefix}F: {node.name}({args_str})")
        
        docstring = ast.get_docstring(node)
        if docstring:
            self.indent_level += 1
            short_doc = docstring.split('\n')[0].strip()
            self._log(f"\"\"\"{short_doc}...\"\"\"")
            self.indent_level -= 1

    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit(child)

# --- Helper Legacy per TOON non-light (struttura scheletrica) ---
# (Qui potresti voler spostare anche questi nei parser in futuro, 
# ma per ora ci concentriamo sulla modalità --light)

def _handle_markdown(content: str) -> str:
    lines = [l.strip() for l in content.splitlines() if l.strip().startswith("#")]
    return "\n".join(lines) or "(Markdown file with no headers)"

def _handle_database_toon(file_path: str) -> str:
    if is_sqlite_database(file_path):
        try:
            schema = get_database_schema(file_path)
            return generate_database_context_toon(schema, os.path.basename(file_path))
        except Exception as e:
            return f"(DB Error: {e})"
    return "(Not a valid SQLite database)"

# ---------------------------------------------------------------------------
# Funzione pubblica principale — LIGHT (solo firme)
# ---------------------------------------------------------------------------

def generate_light_representation(file_path: str, content: str) -> str:
    """
    Genera una rappresentazione LIGHT usando il nuovo sistema di plugin/parser.
    """
    # 1. Gestione Database (caso speciale, non basato su contenuto testo)
    if is_sqlite_database(file_path):
        return _handle_database_toon(file_path)

    # 2. Usa il registro per trovare il parser corretto
    return registry.parse_file(file_path, content)

def get_light_mode_warnings() -> str:
    """
    Restituisce i warning accumulati durante l'esecuzione (es. linguaggi non supportati).
    Da chiamare in main.py se si vuole stampare un header.
    """
    return registry.get_unsupported_warning()

# ---------------------------------------------------------------------------
# Funzione pubblica principale — TOON (skeleton legacy)
# ---------------------------------------------------------------------------

def generate_toon_representation(file_path: str, content: str) -> str:
    """
    Genera una rappresentazione TOON (Token Oriented - Skeleton)
    Mantiene la logica originale per ora, o delega a Light se preferisci unificare.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if is_sqlite_database(file_path):
        return _handle_database_toon(file_path)

    if ext == ".py":
        try:
            tree = ast.parse(content)
            visitor = ToonVisitor()
            visitor.visit(tree)
            return "\n".join(visitor.output)
        except SyntaxError:
            return f"(Syntax Error parsing {os.path.basename(file_path)})"
    
    elif ext in [".md", ".markdown"]:
        return _handle_markdown(content)
        
    # Per semplicità, per ora il Toon standard per altri file 
    # può usare il fallback del nuovo sistema o la vecchia logica.
    # Usiamo il fallback del registry per coerenza:
    return registry.parse_file(file_path, content)

# ---------------------------------------------------------------------------
# Helper per database in focus mode
# ---------------------------------------------------------------------------

def generate_database_focused(file_path: str, focused_tables: list = None) -> str:
    from deepbase.database import generate_database_context_full, generate_database_context_hybrid
    if not is_sqlite_database(file_path):
        return "(Not a valid SQLite database)"
    try:
        schema = get_database_schema(file_path)
        db_name = os.path.basename(file_path)
        if focused_tables:
            return generate_database_context_hybrid(schema, db_name, focused_tables)
        else:
            return generate_database_context_full(schema, db_name)
    except Exception as e:
        return f"(Error processing database: {e})"

--- END OF FILE: src/deepbase/toon.py ---
----------------------------------------

--- START OF FILE: src/deepbase/parsers/__init__.py ---

# src/deepbase/parsers/__init__.py
from .document import get_document_structure
from .registry import registry

# Espone anche le classi se necessario in futuro
__all__ = ['get_document_structure', 'registry']

--- END OF FILE: src/deepbase/parsers/__init__.py ---
----------------------------------------

--- START OF FILE: src/deepbase/parsers/document.py ---

# src/deepbase/parsers/document.py
import re
import os
from .interface import LanguageParser

class MarkdownParser(LanguageParser):
    def parse(self, content: str, file_path: str) -> str:
        lines = []
        for line in content.splitlines():
            if line.strip().startswith("#"):
                lines.append(line.strip())
        if not lines:
            return "(Markdown file with no headers)"
        return "\n".join(lines)

class LatexParser(LanguageParser):
    def parse(self, content: str, file_path: str) -> str:
        keep_patterns = [
            r'^\s*\\documentclass',
            r'^\s*\\usepackage',
            r'^\s*\\input',
            r'^\s*\\include',
            r'^\s*\\(part|chapter|section|subsection|subsubsection)',
            r'^\s*\\begin',
            r'^\s*\\end',
            r'^\s*\\title',
            r'^\s*\\author',
            r'^\s*\\date'
        ]
        combined_pattern = re.compile('|'.join(keep_patterns))
        lines = []
        for line in content.splitlines():
            # Rimuovi commenti inline parziali se necessario, qui semplifichiamo
            line_clean = line.split('%')[0].rstrip()
            if combined_pattern.match(line_clean):
                lines.append(line_clean)
        if not lines:
            return "(LaTeX content empty or purely textual)"
        return "\n".join(lines)

# Istanziamo i parser per uso interno
_md_parser = MarkdownParser()
_tex_parser = LatexParser()

def get_document_structure(file_path: str, content: str):
    """
    Funzione di compatibilità per main.py.
    Restituisce la struttura se è un documento supportato, altrimenti None.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext in ['.md', '.markdown']:
        return _md_parser.parse(content, file_path)
    elif ext in ['.tex', '.sty', '.cls']:
        return _tex_parser.parse(content, file_path)
    
    return None

--- END OF FILE: src/deepbase/parsers/document.py ---
----------------------------------------

--- START OF FILE: src/deepbase/parsers/fallback.py ---

# src/deepbase/parsers/fallback.py
from .interface import LanguageParser

class FallbackParser(LanguageParser):
    """
    Parser generico per file non supportati specificamente.
    Tenta di restituire una versione minimizzata o troncata.
    """
    def parse(self, content: str, file_path: str) -> str:
        lines = []
        # Rimuove righe vuote e commenti base
        for line in content.splitlines():
            clean = line.strip()
            if clean and not clean.startswith("#"):
                lines.append(clean)
        
        if not lines:
            return "(Empty or comments-only file)"
            
        # Se il file Ã¨ molto lungo, troncalo per il fallback
        if len(lines) > 20:
            preview = "\n".join(lines[:20])
            return f"{preview}\n... ({len(lines)-20} more lines hidden - Light Mode Fallback)"
            
        return "\n".join(lines)

--- END OF FILE: src/deepbase/parsers/fallback.py ---
----------------------------------------

--- START OF FILE: src/deepbase/parsers/interface.py ---

# src/deepbase/parsers/interface.py
from abc import ABC, abstractmethod

class LanguageParser(ABC):
    """
    Interfaccia base per i parser di linguaggio.
    """
    
    @abstractmethod
    def parse(self, content: str, file_path: str) -> str:
        """
        Parsa il contenuto del file e restituisce una rappresentazione 'light' (firme, struttura).
        """
        pass

--- END OF FILE: src/deepbase/parsers/interface.py ---
----------------------------------------

--- START OF FILE: src/deepbase/parsers/python.py ---

# src/deepbase/parsers/python.py
import ast
import os
from .interface import LanguageParser

def _extract_module_comments(source: str) -> str:
    """
    Estrae i commenti # e la docstring di modulo dalle prime righe del sorgente.
    """
    lines = []
    in_docstring = False
    docstring_char = None
    source_lines = source.splitlines()

    for line in source_lines:
        stripped = line.strip()

        # Riga vuota: la includiamo solo se siamo giÃ  dentro i commenti iniziali
        if not stripped:
            if lines:
                lines.append("")
            continue

        # Commenti # semplici
        if stripped.startswith("#") and not in_docstring:
            lines.append(line.rstrip())
            continue

        # Inizio docstring di modulo (""" o ''')
        if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
            docstring_char = stripped[:3]
            in_docstring = True
            lines.append(line.rstrip())
            # Docstring su singola riga
            rest = stripped[3:]
            if rest.endswith(docstring_char) and len(rest) >= 3:
                in_docstring = False
            continue

        if in_docstring:
            lines.append(line.rstrip())
            if stripped.endswith(docstring_char):
                in_docstring = False
            continue

        # Qualsiasi altra cosa: fine dell'header
        break

    # Rimuovi trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines)


class LightVisitor(ast.NodeVisitor):
    """
    Visita l'AST e produce le firme dei metodi/funzioni Python.
    """

    def __init__(self):
        self.output = []
        self.indent_level = 0

    def _log(self, text):
        indent = "    " * self.indent_level
        self.output.append(f"{indent}{text}")

    def visit_ClassDef(self, node):
        self._log(f"class {node.name}:")
        self.indent_level += 1

        # Docstring della classe (prima riga)
        docstring = ast.get_docstring(node)
        if docstring:
            first_line = docstring.split('\n')[0].strip()
            self._log(f'"""{first_line}"""')

        self.generic_visit(node)
        self.indent_level -= 1

    def visit_FunctionDef(self, node):
        self._emit_signature(node, is_async=False)

    def visit_AsyncFunctionDef(self, node):
        self._emit_signature(node, is_async=True)

    def _emit_signature(self, node, is_async: bool):
        prefix = "async " if is_async else ""

        # --- Argomenti con annotazioni di tipo ---
        args_parts = []
        all_args = node.args.args
        defaults = node.args.defaults
        defaults_offset = len(all_args) - len(defaults)

        for i, arg in enumerate(all_args):
            arg_str = arg.arg
            if arg.annotation:
                try:
                    arg_str += f": {ast.unparse(arg.annotation)}"
                except Exception:
                    # Fallback per vecchie versioni python o AST complessi
                    pass
            default_idx = i - defaults_offset
            if default_idx >= 0:
                try:
                    default_val = ast.unparse(defaults[default_idx])
                    arg_str += f" = {default_val}"
                except Exception:
                    arg_str += " = ..."
            args_parts.append(arg_str)

        # *args
        if node.args.vararg:
            va = node.args.vararg
            va_str = f"*{va.arg}"
            if va.annotation:
                try:
                    va_str += f": {ast.unparse(va.annotation)}"
                except Exception:
                    pass
            args_parts.append(va_str)

        # keyword-only args
        kwonly_defaults = {
            i: node.args.kw_defaults[i]
            for i in range(len(node.args.kwonlyargs))
            if node.args.kw_defaults[i] is not None
        }
        for i, kwarg in enumerate(node.args.kwonlyargs):
            kw_str = kwarg.arg
            if kwarg.annotation:
                try:
                    kw_str += f": {ast.unparse(kwarg.annotation)}"
                except Exception:
                    pass
            if i in kwonly_defaults:
                try:
                    kw_str += f" = {ast.unparse(kwonly_defaults[i])}"
                except Exception:
                    kw_str += " = ..."
            args_parts.append(kw_str)

        # **kwargs
        if node.args.kwarg:
            kwa = node.args.kwarg
            kwa_str = f"**{kwa.arg}"
            if kwa.annotation:
                try:
                    kwa_str += f": {ast.unparse(kwa.annotation)}"
                except Exception:
                    pass
            args_parts.append(kwa_str)

        args_str = ", ".join(args_parts)

        # --- Tipo di ritorno ---
        ret_anno = ""
        if node.returns:
            try:
                ret_anno = f" -> {ast.unparse(node.returns)}"
            except Exception:
                pass

        self._log(f"{prefix}def {node.name}({args_str}){ret_anno}: ...")

        # Docstring della funzione (prima riga)
        docstring = ast.get_docstring(node)
        if docstring:
            first_line = docstring.split('\n')[0].strip()
            self.indent_level += 1
            self._log(f'"""{first_line}"""')
            self.indent_level -= 1

    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit(child)


class PythonParser(LanguageParser):
    def parse(self, content: str, file_path: str) -> str:
        filename = os.path.basename(file_path)
        try:
            tree = ast.parse(content)
            visitor = LightVisitor()
            visitor.visit(tree)
            signatures = "\n".join(visitor.output)

            # Prepend commenti/docstring iniziali del modulo
            module_header = _extract_module_comments(content)
            
            parts = []
            if module_header:
                parts.append(module_header)
            if signatures:
                parts.append(signatures)
                
            result = "\n\n".join(parts)
            return result.strip() or f"(No functions or classes found in {filename})"
        except SyntaxError:
            return f"(Syntax Error parsing {filename})"
        except Exception as e:
            return f"(Error parsing Python file: {e})"

--- END OF FILE: src/deepbase/parsers/python.py ---
----------------------------------------

--- START OF FILE: src/deepbase/parsers/registry.py ---

# src/deepbase/parsers/registry.py
import os
from typing import Dict, Set
from .interface import LanguageParser
from .python import PythonParser
from .document import MarkdownParser, LatexParser  # <--- Importa i nuovi parser
from .fallback import FallbackParser

class ParserRegistry:
    def __init__(self):
        self._parsers: Dict[str, LanguageParser] = {}
        self._fallback = FallbackParser()
        self._unsupported_extensions_encountered: Set[str] = set()
        
        # Registrazione parser
        self.register_parser('.py', PythonParser())
        
        # Registrazione Documenti
        md_parser = MarkdownParser()
        self.register_parser('.md', md_parser)
        self.register_parser('.markdown', md_parser)
        
        tex_parser = LatexParser()
        for ext in ['.tex', '.sty', '.cls']:
            self.register_parser(ext, tex_parser)
        
    def register_parser(self, extension: str, parser: LanguageParser):
        self._parsers[extension] = parser

    def get_parser(self, file_path: str) -> LanguageParser:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext in self._parsers:
            return self._parsers[ext]
        
        if ext:
            self._unsupported_extensions_encountered.add(ext)
            
        return self._fallback

    def parse_file(self, file_path: str, content: str) -> str:
        parser = self.get_parser(file_path)
        return parser.parse(content, file_path)

    def get_unsupported_warning(self) -> str:
        if not self._unsupported_extensions_encountered:
            return ""
        ext_list = ", ".join(sorted(self._unsupported_extensions_encountered))
        return (
            f"> [WARNING] Light Mode support is currently limited for: {ext_list}. "
            "Using generic fallback for these files.\n"
        )

registry = ParserRegistry()

--- END OF FILE: src/deepbase/parsers/registry.py ---
----------------------------------------

--- START OF FILE: docs/index.md ---

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

--- END OF FILE: docs/index.md ---
----------------------------------------

--- START OF FILE: docs/reference.md ---

# API Reference

## Main Module

::: deepbase.main

--- END OF FILE: docs/reference.md ---
----------------------------------------

