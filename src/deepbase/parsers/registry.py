# src/deepbase/parsers/registry.py
import os
from typing import Dict, Set
from .interface import LanguageParser
from .python import PythonParser
from .javascript import JavaScriptParser  # <--- NUOVO IMPORT
from .document import MarkdownParser, LatexParser
from .fallback import FallbackParser

class ParserRegistry:
    def __init__(self):
        self._parsers: Dict[str, LanguageParser] = {}
        self._fallback = FallbackParser()
        self._unsupported_extensions_encountered: Set[str] = set()
        
        # --- Python ---
        self.register_parser('.py', PythonParser())
        
        # --- JavaScript / TypeScript / React Native ---
        js_parser = JavaScriptParser()
        # Copre tutto l'ecosistema React/Node/TS
        for ext in ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs']:
            self.register_parser(ext, js_parser)
        
        # --- Documentazione ---
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