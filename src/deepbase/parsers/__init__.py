# src/deepbase/parsers/__init__.py
from .document import get_document_structure
from .registry import registry

# Espone anche le classi se necessario in futuro
__all__ = ['get_document_structure', 'registry']