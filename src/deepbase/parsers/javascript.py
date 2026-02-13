# src/deepbase/parsers/javascript.py
import re
from .interface import LanguageParser

class JavaScriptParser(LanguageParser):
    """
    Parser per JavaScript, TypeScript e React Native (.js, .jsx, .ts, .tsx).
    Usa regex per identificare firme di funzioni, classi, interfacce e componenti React.
    """

    def parse(self, content: str, file_path: str) -> str:
        lines = []
        
        # Regex patterns per catturare le definizioni
        patterns = [
            # Class definition (es. export default class MyClass extends Component)
            re.compile(r'^\s*(export\s+)?(default\s+)?(abstract\s+)?class\s+([a-zA-Z0-9_]+)(.*)?\{'),
            
            # Function definition standard (es. async function myFunc(a, b))
            re.compile(r'^\s*(export\s+)?(default\s+)?(async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(.*'),
            
            # Arrow Function / Variable Assignments (es. const MyComponent = (props) => {)
            # Cattura costanti che sembrano funzioni o componenti React
            re.compile(r'^\s*(export\s+)?(const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(async\s*)?(\(.*\)|[^=]+)\s*=>.*'),
            
            # TypeScript Interfaces & Types
            re.compile(r'^\s*(export\s+)?(interface|type)\s+([a-zA-Z0-9_]+).*'),
            
            # React Hooks (opzionale: spesso sono implementation details, 
            # ma custom hooks 'useSomething' top-level potrebbero essere rilevanti. 
            # Per ora li ignoriamo per risparmiare token, tenendo solo le definizioni)
        ]

        # JSDoc pattern (multiline)
        in_comment = False
        
        source_lines = content.splitlines()
        
        for i, line in enumerate(source_lines):
            stripped = line.strip()
            
            # Gestione commenti JSDoc /** ... */
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

            # Verifica se la riga matcha una definizione importante
            is_match = False
            for pattern in patterns:
                # Usiamo match sulla riga pulita o search per flessibilità
                if pattern.match(stripped):
                    # Pulizia fine riga: se finisce con '{', lo sostituiamo con '...'
                    clean_line = stripped
                    if clean_line.endswith("{"):
                        clean_line = clean_line[:-1].strip()
                    
                    # Aggiunge firma + ...
                    lines.append(f"{clean_line} {{ ... }}")
                    is_match = True
                    break
            
            # Fallback per decoratori (es. @Component in Angular o NestJS, usati anche in RN con mobx)
            if not is_match and stripped.startswith("@"):
                # Mantiene il decoratore se è seguito da una classe nella riga successiva (euristica semplice)
                if i + 1 < len(source_lines) and "class " in source_lines[i+1]:
                    lines.append(stripped)

        if not lines:
            return f"(No exported functions, classes or components found in {file_path})"

        return "\n".join(lines)