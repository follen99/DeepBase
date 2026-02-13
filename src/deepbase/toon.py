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