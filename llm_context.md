# Project Context: DeepBase

### PROJECT STRUCTURE

Project Structure in: /home/follen/Documents/git-local/DeepBase

📂 ./
    📄 .gitignore
    📄 README.md
    📄 llm_context.md
    📄 mkdocs.yml
    📄 pyproject.toml
    📂 examples/
        📄 deepbase_context.md
    📂 tests/
        📄 test_cli.py
        📄 test_parsers.py
    📂 src/
        📂 deepbase/
            📄 __init__.py
            📄 main.py
            📄 parsers.py
            📄 toon.py
        📂 deepbase.egg-info/
    📂 docs/
        📄 index.md
        📄 reference.md


### SEMANTIC SKELETONS (TOON)

> FILE: .gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
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
*.manifest
*.spec
debug.log
pip-log.txt
pip-delete-this-directory.txt
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
*.mo
*.pot
*.log
local_settings.py
db.sqlite3
instance/
.webassets-cache
.scrapy
docs/_build/
.target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.python-version
__pypackages__/
celerybeat-schedule
*.sage.py
.env
.venv
env.bak
venv.bak
.spyderproject
.spyproject
.ropeproject
/site
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
cython_debug/
.abstra/
.ruff_cache/
.pypirc
.cursorignore
.cursorindexingignore
marimo/_static/
marimo/_lsp/
__marimo__/
> FILE: README.md
# DeepBase
## Features
## Installation
## How to Use
### Advanced Configuration
# Add more directories to ignore.
# These will be added to the default ones.
# Add more extensions or filenames to include.
### Single File Analysis (New!)
# Generates "llm_context.md" containing only the headers tree.
# Generates "llm_context.md" containing the outline followed by the full text.
## Development Workflow
### 1. Local Setup & Testing
# Install in editable mode
# Run tests
# Test the tool locally without reinstalling
# You can now use the 'deepbase' command directly and it reflects your code changes immediately.
### 2. Release Process
## License
> FILE: llm_context.md
(Markdown file with no headers)
> FILE: mkdocs.yml
site_name:
site_description:
site_url:
repo_url:
repo_name:
theme:
  name:
  palette:
    - scheme:
      primary:
      accent:
      toggle:
        icon:
        name:
    - scheme:
      primary:
      accent:
      toggle:
        icon:
        name:
  features:
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths:
nav:
  - Home:
  - API Reference:
> FILE: pyproject.toml
[build-system]
requires = ...
build-backend = ...
[project]
name = ...
version = ...
authors = ...
{ name = ...
description = ...
readme = ...
license = ...
requires-python = ...
classifiers = ...
keywords = ...
dependencies = ...
[project.urls]
"Homepage" = ...
"Bug Tracker" = ...
[project.scripts]
deepbase = ...
[project.optional-dependencies]
dev = ...
docs = ...
"mkdocs> = ...
"mkdocs-material> = ...
"mkdocstrings[python]> = ...
> FILE: examples/deepbase_context.md
# Project Context: DeepBase
### PROJECT STRUCTURE ###
### FILE CONTENTS ###
# Byte-compiled / optimized / DLL files
# C extensions
# Distribution / packaging
# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
# Installer logs
# Unit test / coverage reports
# Translations
# Django stuff:
# Flask stuff:
# Scrapy stuff:
# Sphinx documentation
# PyBuilder
# Jupyter Notebook
# IPython
# pyenv
# pipenv
# According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
# However, in case you generate it automatically, you may want to ignore it.
# Pipfile.lock
# poetry
# According to python-poetry/poetry#519, it is recommended to include poetry.lock in version control.
# This is especially if you are building a library.
# poetry.lock
# PEP 582; used by e.g. github.com/David-OConnor/pyflow
# Celery stuff
# SageMath parsed files
# Environments
# Spyder project settings
# Rope project settings
# mkdocs documentation
# mypy
# Pyre type checker
# pytype static type analyzer
# Cython debug symbols
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
# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer,
#  you could uncomment the following to ignore the entire vscode folder
# .vscode/
# Ruff stuff:
# PyPI configuration file
# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
# Marimo
# DeepBase
## Features
## Installation
## How to Use
### Advanced Configuration
# Add more directories to ignore.
# These will be added to the default ones.
# Add more extensions or filenames to include.
## License
# pyproject.toml
# Increment the version to reflect changes
# Main project dependencies
# Update the script to point to the Typer app object
# Optional dependencies for development (e.g., testing)
# src/deepbase/main.py
# --- DEFAULT CONFIGURATION ---
# --- TOOL INITIALIZATION ---
# Merge user config with defaults
# 1. Write the header
# 2. Write the structure
# 3. Write the file contents
# Detect encoding
# Read and write content with robust error handling
# Project Context: DeepBase
### PROJECT STRUCTURE ###
### FILE CONTENTS ###
# Byte-compiled / optimized / DLL files
# C extensions
# Distribution / packaging
# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
# Installer logs
# Unit test / coverage reports
# Translations
# Django stuff:
# Flask stuff:
# Scrapy stuff:
# Sphinx documentation
# PyBuilder
# Jupyter Notebook
# IPython
# pyenv
# pipenv
# According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
# However, in case you generate it automatically, you may want to ignore it.
# Pipfile.lock
# poetry
# According to python-poetry/poetry#519, it is recommended to include poetry.lock in version control.
# This is especially if you are building a library.
# poetry.lock
# PEP 582; used by e.g. github.com/David-OConnor/pyflow
# Celery stuff
# SageMath parsed files
# Environments
# Spyder project settings
# Rope project settings
# mkdocs documentation
# mypy
# Pyre type checker
# pytype static type analyzer
# Cython debug symbols
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
# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer,
#  you could uncomment the following to ignore the entire vscode folder
# .vscode/
# Ruff stuff:
# PyPI configuration file
# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
# Marimo
# DeepBase
## Features
## Installation
## How to Use
### Advanced Configuration
# Add more directories to ignore.
# These will be added to the default ones.
# Add more extensions or filenames to include.
## License
# pyproject.toml
# Increment the version to reflect changes
# Main project dependencies
# Update the script to point to the Typer app object
# Optional dependencies for development (e.g., testing)
# tests/test_main.py
# Runner instance to execute Typer app commands
# 1. Create a mock project structure
# Create a directory to ignore
# 2. Execute the CLI command with arguments in the correct order
# 3. Verify the results
# Check that significant files are included
# Check that ignored directory and files are not present
> FILE: tests/test_cli.py
F: test_cli_single_file_default(tmp_path)
  """Testa che di default (senza -a) venga generata SOLO la struttura...."""
F: test_cli_single_file_with_all(tmp_path)
  """Testa che con il flag --all venga generato ANCHE il contenuto...."""
> FILE: tests/test_parsers.py
F: test_extract_markdown_structure_simple()
  """Testa l'estrazione corretta di header semplici...."""
F: test_extract_markdown_structure_no_headers()
  """Testa un file markdown senza intestazioni...."""
F: test_extract_markdown_structure_complex()
  """Testa che il codice e i commenti non vengano confusi per header...."""
F: test_dispatcher_extensions()
  """Testa che il dispatcher scelga il parser giusto in base all'estensione...."""
> FILE: src/deepbase/__init__.py

> FILE: src/deepbase/main.py
F: load_config(root_dir)
F: is_significant_file(file_path, significant_extensions) -> bool
F: generate_directory_tree(root_dir, config) -> str
F: get_all_significant_files(root_dir, config)
F: read_file_content(file_path) -> str
F: create(target, output, verbose, include_all, toon_mode)
  """Analyzes a directory OR a single file...."""
> FILE: src/deepbase/parsers.py
F: extract_markdown_structure(content) -> str
  """Estrae solo le intestazioni (headers) da un contenuto Markdown,..."""
F: get_document_structure(file_path, content)
  """Funzione dispatcher che decide quale parser usare in base all'estensione...."""
> FILE: src/deepbase/toon.py
C: ToonVisitor
  F: __init__(self)
  F: _log(self, text)
  F: visit_ClassDef(self, node)
  F: visit_FunctionDef(self, node)
  F: visit_AsyncFunctionDef(self, node)
  F: _handle_function(self, node, is_async)
  F: generic_visit(self, node)
F: _handle_markdown(content) -> str
  """Estrae solo gli header Markdown...."""
F: _handle_toml_ini(content) -> str
  """Estrae sezioni [Title] e chiavi, ignorando valori lunghi...."""
F: _handle_json_structure(content) -> str
  """Prova a parsare JSON e restituire solo le chiavi di primo/secondo livello...."""
F: _handle_minified_config(content) -> str
  """Rimuove righe vuote e commenti (per .gitignore, requirements.txt)...."""
F: generate_toon_representation(file_path, content) -> str
  """Genera una rappresentazione TOON (Token Oriented) in base al tipo di file...."""
> FILE: docs/index.md
# DeepBase
## Features
## Installation
## How to Use
### Advanced Configuration
# Add more directories to ignore.
# These will be added to the default ones.
# Add more extensions or filenames to include.
## License
> FILE: docs/reference.md
# API Reference
## Main Module
