# File Structure Analysis: README.md

================================================================================
### DOCUMENT STRUCTURE (Outline) ###
================================================================================

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

================================================================================
### FILE CONTENT ###
================================================================================

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

### Single File Analysis (New!)

DeepBase supports analyzing a single specific file.

**1. Structure Only (Default)**
By default, providing a single file will extract only its outline/structure (headers). This is useful for quickly understanding the organization of a large document without reading everything.

```sh
deepbase README.md
# Generates "llm_context.md" containing only the headers tree.
```

**2. Structure + Content**
If you want both the structure outline AND the full file content appended at the end, use the `--all` (or `-a`) flag.

```sh
deepbase README.md --all
# Generates "llm_context.md" containing the outline followed by the full text.
```

*Currently optimized for Markdown files.*


## Development Workflow

If you want to contribute or test the tool locally, follow these steps.

### 1. Local Setup & Testing
Clones the repo and installs the package in "editable" mode with development dependencies.

```sh
# Install in editable mode
pip install -e ".[dev]"

# Run tests
pytest

# Test the tool locally without reinstalling
# You can now use the 'deepbase' command directly and it reflects your code changes immediately.
deepbase ./README.md
```

### 2. Release Process
To create a new release (which triggers the PyPI deployment pipeline):

1.  **Update Version**: Bump the version number in `pyproject.toml` (e.g., `1.2.0` -> `1.3.0`).
2.  **Commit & Push**:
    ```sh
    git add pyproject.toml
    git commit -m "Bump version to 1.3.0"
    git push origin main
    ```
3.  **Create a Tag**: This usually triggers the CI/CD pipeline.
    ```sh
    git tag v1.3.0
    git push origin v1.3.0
    ```
4.  **GitHub Release**: Go to GitHub releases page and draft a new release from the tag.

*Currently optimized for Markdown files. Support for `.docx` and `.tex` structure extraction is coming soon.*

## License

This project is released under the GPL 3 license. See the `LICENSE` file for details.

--- END OF FILE: README.md ---
