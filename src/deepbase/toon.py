# src/deepbase/toon.py

import ast
import os
import re
import json

# Import database handling
from deepbase.database import (
    get_database_schema,
    generate_database_context_toon,
    generate_database_context_hybrid,
    is_sqlite_database
)


# ---------------------------------------------------------------------------
# TOON VISITOR — mantiene classi + firme + docstring (comportamento originale)
# ---------------------------------------------------------------------------

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

        ret_anno = ""
        if node.returns:
            try:
                if isinstance(node.returns, ast.Name):
                    ret_anno = f" -> {node.returns.id}"
                elif isinstance(node.returns, ast.Constant):
                    ret_anno = f" -> {node.returns.value}"
            except Exception:
                pass

        self._log(f"{prefix}F: {node.name}({args_str}){ret_anno}")

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


# ---------------------------------------------------------------------------
# LIGHT VISITOR — solo firme Python con docstring/commenti iniziali
# ---------------------------------------------------------------------------

def _extract_module_comments(source: str) -> str:
    """
    Estrae i commenti # e la docstring di modulo dalle prime righe del sorgente.
    Si ferma al primo costrutto non-commento e non-docstring.
    """
    lines = []
    in_docstring = False
    docstring_char = None
    source_lines = source.splitlines()

    for line in source_lines:
        stripped = line.strip()

        # Riga vuota: la includiamo solo se siamo già dentro i commenti iniziali
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
    Visita l'AST e produce le firme dei metodi/funzioni Python,
    preservando la corretta indentazione per classi nidificate.
    Include la prima riga di docstring di classi e funzioni come commento.
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
        """Emette la firma completa della funzione/metodo in stile Python."""
        prefix = "async " if is_async else ""

        # --- Argomenti con annotazioni di tipo ---
        args_parts = []

        all_args = node.args.args
        defaults = node.args.defaults
        defaults_offset = len(all_args) - len(defaults)

        for i, arg in enumerate(all_args):
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            default_idx = i - defaults_offset
            if default_idx >= 0:
                default_val = ast.unparse(defaults[default_idx])
                arg_str += f" = {default_val}"
            args_parts.append(arg_str)

        # *args
        if node.args.vararg:
            va = node.args.vararg
            va_str = f"*{va.arg}"
            if va.annotation:
                va_str += f": {ast.unparse(va.annotation)}"
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
                kw_str += f": {ast.unparse(kwarg.annotation)}"
            if i in kwonly_defaults:
                kw_str += f" = {ast.unparse(kwonly_defaults[i])}"
            args_parts.append(kw_str)

        # **kwargs
        if node.args.kwarg:
            kwa = node.args.kwarg
            kwa_str = f"**{kwa.arg}"
            if kwa.annotation:
                kwa_str += f": {ast.unparse(kwa.annotation)}"
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

        # Docstring della funzione (prima riga, indentata sotto la firma)
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


# ---------------------------------------------------------------------------
# Gestori per file Non-Python
# ---------------------------------------------------------------------------

def _handle_markdown(content: str) -> str:
    """Estrae solo gli header Markdown."""
    lines = []
    for line in content.splitlines():
        if line.strip().startswith("#"):
            lines.append(line.strip())
    if not lines:
        return "(Markdown file with no headers)"
    return "\n".join(lines)


def _handle_toml_ini(content: str) -> str:
    """Estrae sezioni [Title] e chiavi, ignorando valori lunghi."""
    lines = []
    for line in content.splitlines():
        clean = line.strip()
        if not clean or clean.startswith("#"):
            continue
        if clean.startswith("[") and clean.endswith("]"):
            lines.append(clean)
        elif "=" in clean:
            key = clean.split("=")[0].strip()
            lines.append(f"{key} = ...")
    return "\n".join(lines)


def _handle_json_structure(content: str) -> str:
    """Prova a parsare JSON e restituire solo le chiavi di primo/secondo livello."""
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            lines = ["{"]
            for k, v in data.items():
                if isinstance(v, dict):
                    lines.append(f"  {k}: {{ ...keys: {list(v.keys())} }}")
                elif isinstance(v, list):
                    lines.append(f"  {k}: [ ...size: {len(v)} ]")
                else:
                    lines.append(f"  {k}: (value)")
            lines.append("}")
            return "\n".join(lines)
        return "(JSON Array or Scalar)"
    except Exception:
        return "(Invalid JSON content)"


def _handle_minified_config(content: str) -> str:
    """Rimuove righe vuote e commenti (per .gitignore, requirements.txt)."""
    lines = []
    for line in content.splitlines():
        clean = line.strip()
        if clean and not clean.startswith("#"):
            lines.append(clean)
    if not lines:
        return "(Empty or comments-only file)"
    return "\n".join(lines)


def _handle_latex_structure(content: str) -> str:
    """
    Minimizza il LaTeX mantenendo struttura, pacchetti e comandi chiave.
    Rimuove il testo semplice.
    """
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
        line = line.split('%')[0].rstrip()
        if combined_pattern.match(line):
            lines.append(line)
    if not lines:
        return "(LaTeX content empty or purely textual)"
    return "\n".join(lines)


def _handle_database_toon(file_path: str) -> str:
    """Handle database files in TOON mode."""
    if is_sqlite_database(file_path):
        try:
            schema = get_database_schema(file_path)
            return generate_database_context_toon(schema, os.path.basename(file_path))
        except Exception as e:
            return f"(DB Error: {e})"
    return "(Not a valid SQLite database)"


# ---------------------------------------------------------------------------
# Funzione pubblica principale — TOON (skeleton completo)
# ---------------------------------------------------------------------------

def generate_toon_representation(file_path: str, content: str) -> str:
    """
    Genera una rappresentazione TOON (Token Oriented) in base al tipo di file.
    Include classi, firme e docstring.
    """
    _, ext = os.path.splitext(file_path)
    filename = os.path.basename(file_path)
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
            return f"(Syntax Error parsing {filename})"

    elif ext in [".md", ".markdown"]:
        return _handle_markdown(content)

    elif ext in [".tex", ".sty", ".cls"]:
        return _handle_latex_structure(content)

    elif ext in [".toml", ".ini", ".cfg"]:
        return _handle_toml_ini(content)

    elif ext == ".json":
        return _handle_json_structure(content)

    elif ext in [".txt", ".dockerignore", ".gitignore"] or filename in [".gitignore", ".dockerignore", "Dockerfile", "Makefile"]:
        return _handle_minified_config(content)

    elif ext in [".yml", ".yaml"]:
        lines = [line for line in content.splitlines() if ":" in line and not line.strip().startswith("#")]
        clean_lines = []
        for l in lines:
            key = l.split(":")[0]
            clean_lines.append(f"{key}:")
        return "\n".join(clean_lines)

    else:
        minified = _handle_minified_config(content)
        lines = minified.splitlines()
        if len(lines) > 10:
            return "\n".join(lines[:10]) + f"\n... ({len(lines)-10} more meaningful lines hidden)"
        return minified


# ---------------------------------------------------------------------------
# Funzione pubblica principale — LIGHT (solo firme)
# ---------------------------------------------------------------------------

def generate_light_representation(file_path: str, content: str) -> str:
    """
    Genera una rappresentazione LIGHT: solo le firme dei metodi/funzioni.
    Per file Python: usa LightVisitor (def/async def con tipi, niente corpo)
    preceduto dai commenti/docstring di modulo iniziali.
    Per altri tipi di file: delega alla rappresentazione TOON standard,
    perché per file non-Python non c'è distinzione tra "firma" e "scheletro".
    """
    _, ext = os.path.splitext(file_path)
    filename = os.path.basename(file_path)
    ext = ext.lower()

    # DATABASE: stessa logica TOON (schema compatto)
    if is_sqlite_database(file_path):
        return _handle_database_toon(file_path)

    # PYTHON: commenti di modulo + firme via LightVisitor
    if ext == ".py":
        try:
            tree = ast.parse(content)
            visitor = LightVisitor()
            visitor.visit(tree)
            signatures = "\n".join(visitor.output)

            # Prepend commenti/docstring iniziali del modulo (se presenti)
            module_header = _extract_module_comments(content)
            if module_header:
                result = module_header + "\n\n" + signatures
            else:
                result = signatures

            return result.strip() or f"(No functions or classes found in {filename})"
        except SyntaxError:
            return f"(Syntax Error parsing {filename})"

    # Tutti gli altri tipi: delega al TOON standard
    # (markdown -> headers, toml -> chiavi, json -> struttura, ecc.)
    return generate_toon_representation(file_path, content)


# ---------------------------------------------------------------------------
# Helper per database in focus mode (usato da main.py)
# ---------------------------------------------------------------------------

def generate_database_focused(file_path: str, focused_tables: list = None) -> str:
    """
    Generate database context with specific tables in full detail.
    Used when database is in focus mode.
    """
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