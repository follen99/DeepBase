# src/deepbase/parsers/javascript.py
import re
from .interface import LanguageParser

class JavaScriptParser(LanguageParser):
    """
    Parser per JavaScript, TypeScript e React Native (.js, .jsx, .ts, .tsx).
    Versione 1.1: Logica Regex base + Supporto Export Default.
    """

    def parse(self, content: str, file_path: str) -> str:
        lines = []
        
        # Regex patterns per catturare le definizioni strutturali (classi, funzioni, var, tipi)
        patterns = [
            # Class definition
            re.compile(r'^\s*(export\s+)?(default\s+)?(abstract\s+)?class\s+([a-zA-Z0-9_]+)(.*)?\{'),
            
            # Function definition standard
            re.compile(r'^\s*(export\s+)?(default\s+)?(async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(.*'),
            
            # Arrow Function / Variable Assignments
            re.compile(r'^\s*(export\s+)?(const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(async\s*)?(\(.*\)|[^=]+)\s*=>.*'),
            
            # TypeScript Interfaces & Types
            re.compile(r'^\s*(export\s+)?(interface|type)\s+([a-zA-Z0-9_]+).*'),
        ]

        # --- NEW: Regex specifica per Export Default diretto (V2 Feature) ---
        # Cattura: export default router; | export default MyComponent;
        # Il (?!...) assicura che non catturi "class" o "function" che sono gestiti meglio dai pattern sopra.
        re_export_default = re.compile(r'^\s*export\s+default\s+(?!class|function)([a-zA-Z0-9_]+);?')

        # JSDoc pattern
        in_comment = False
        source_lines = content.splitlines()
        
        for i, line in enumerate(source_lines):
            stripped = line.strip()
            
            # Gestione commenti JSDoc
            if stripped.startswith("/**"):
                in_comment = True
                lines.append(stripped)
                if stripped.endswith("*/"): 
                    in_comment = False
                continue
            
            if in_comment:
                lines.append(stripped)
                if stripped.endswith("*/"):
                    in_comment = False
                continue

            # Ignora commenti single line o righe vuote
            if not stripped or stripped.startswith("//"):
                continue

            # --- NEW: Controllo Export Default ---
            # Se è un export default semplice, lo aggiungiamo così com'è (senza { ... })
            if re_export_default.match(stripped):
                lines.append(stripped)
                continue

            # Verifica patterns standard
            is_match = False
            for pattern in patterns:
                if pattern.match(stripped):
                    # Pulizia fine riga: se finisce con '{', lo sostituiamo con '...'
                    clean_line = stripped
                    if clean_line.endswith("{"):
                        clean_line = clean_line[:-1].strip()
                    
                    # Aggiunge firma + { ... } per indicare struttura compressa
                    lines.append(f"{clean_line} {{ ... }}")
                    is_match = True
                    break
            
            # Fallback per decoratori
            if not is_match and stripped.startswith("@"):
                if i + 1 < len(source_lines) and "class " in source_lines[i+1]:
                    lines.append(stripped)

        if not lines:
            return f"(No exported functions, classes or components found in {file_path})"

        return "\n".join(lines)