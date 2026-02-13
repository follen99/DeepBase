# src/deepbase/parsers/interface.py
from abc import ABC, abstractmethod

class LanguageParser(ABC):
    """
    Interfaccia base per i parser di linguaggio.
    """
    
    @abstractmethod
    def parse(self, content: str, file_path: str) -> str:
        """
        Parsa il contenuto del file e restituisce una rappresentazione 'light' (firme, struttura).
        """
        pass