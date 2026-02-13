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