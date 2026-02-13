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
            
        # Se il file è molto lungo, troncalo per il fallback
        if len(lines) > 20:
            preview = "\n".join(lines[:20])
            return f"{preview}\n... ({len(lines)-20} more lines hidden - Light Mode Fallback)"
            
        return "\n".join(lines)