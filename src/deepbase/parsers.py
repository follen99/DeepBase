# src/deepbase/parser.py (AGGIORNAMENTO)

import os
import re
from typing import Optional

# Import database functions
from deepbase.database import (
    get_database_schema, 
    generate_database_context_full,
    generate_database_context_toon,
    is_sqlite_database
)


def extract_markdown_structure(content: str) -> str:
    """Estrae solo le intestazioni (headers) da un contenuto Markdown."""
    lines = []
    # Regex per catturare le righe che iniziano con #
    header_pattern = re.compile(r'^\s*(#{1,6})\s+(.*)')
    
    for line in content.splitlines():
        if header_pattern.match(line):
            lines.append(line.strip())
            
    if not lines:
        return "(Nessuna struttura Markdown rilevata)"
    return "\n".join(lines)


def extract_latex_structure(content: str) -> str:
    """Estrae comandi strutturali LaTeX (part, chapter, section, etc)."""
    lines = []
    # Regex per catturare comandi strutturali standard di LaTeX
    # Supporta \section{Title} e \section*{Title}
    tex_pattern = re.compile(r'^\s*\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\{(.+?)\}')
    
    # Catturiamo anche documentclass e begin/end document per contesto
    context_pattern = re.compile(r'^\s*\\(documentclass|begin|end)\{.+?\}')

    for line in content.splitlines():
        if tex_pattern.match(line) or context_pattern.match(line):
            lines.append(line.strip())
            
    if not lines:
        return "(Nessuna struttura LaTeX rilevata)"
    return "\n".join(lines)


def get_document_structure(file_path: str, content: str) -> Optional[str]:
    """Funzione dispatcher che decide quale parser usare."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # --- DATABASE HANDLER ---
    if ext in ['.db', '.sqlite', '.sqlite3', '.db3'] or is_sqlite_database(file_path):
        if is_sqlite_database(file_path):
            try:
                schema = get_database_schema(file_path)
                return generate_database_context_full(schema, os.path.basename(file_path))
            except Exception as e:
                return f"(Error reading database: {e})"
    
    if ext in ['.md', '.markdown', '.mdown', '.mkd']:
        return extract_markdown_structure(content)
    
    # --- LATEX HANDLER ---
    elif ext in ['.tex']:
        return extract_latex_structure(content)
    
    return None


def get_database_toon(file_path: str) -> Optional[str]:
    """
    Generate TOON representation for database files.
    Called by toon.py when processing databases.
    """
    if is_sqlite_database(file_path):
        try:
            schema = get_database_schema(file_path)
            return generate_database_context_toon(schema, os.path.basename(file_path))
        except Exception as e:
            return f"(DB Error: {e})"
    return None