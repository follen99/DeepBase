# tests/test_suite_python.py

import os
import typer
from typer.testing import CliRunner
from deepbase.main import main

# Creiamo un'app Typer temporanea per il testing
test_app = typer.Typer()
test_app.command()(main)

runner = CliRunner()

class TestPythonSuite:
    """
    Test suite dedicata all'analisi di progetti Python con DeepBase.
    FIX: Specifica sempre l'output path esplicito per evitare FileNotFoundError.
    FIX: Controlla il contenuto del file generato, non lo stdout, per la struttura.
    """

    def create_dummy_python_project(self, root):
        """Helper per popolare una directory con file Python finti."""
        # 1. File principale
        main_py = root / "main.py"
        main_py.write_text("""
import os

def hello_world():
    print("Hello content")
    return True

class MyClass:
    def method_one(self):
        # This is a comment inside
        return 1
""", encoding="utf-8")

        # 2. Modulo utils
        utils_dir = root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def help_me():\n    pass", encoding="utf-8")

        # 3. File da ignorare (segreto)
        (root / "secrets.py").write_text("API_KEY = '123'", encoding="utf-8")

        # 4. Cartella da ignorare (es. cache)
        cache_dir = root / ".mypy_cache"
        cache_dir.mkdir()
        (cache_dir / "data.json").write_text("{}", encoding="utf-8")

    def test_basic_structure(self, tmp_path):
        """Testa che il comando base generi la struttura nel file."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        
        # Passiamo esplicitamente l'output file nel tmp_path
        result = runner.invoke(test_app, [str(tmp_path), "-o", str(output_file)])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica presenza nell'albero (DENTRO IL FILE, non nello stdout)
        assert "main.py" in content
        assert "utils/" in content
        
        # Verifica che il CONTENUTO del codice NON ci sia
        assert "def hello_world" not in content
        assert "import os" not in content

    def test_flag_all_content(self, tmp_path):
        """Testa --all: deve includere tutto il codice."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--all", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # Deve contenere il corpo delle funzioni
        assert "print(\"Hello content\")" in content
        assert "class MyClass:" in content

    def test_flag_light_mode(self, tmp_path):
        """Testa --light: deve includere firme ma NON il corpo."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # Deve contenere la notice Light Mode
        assert "[LIGHT MODE]" in content
        
        # Deve contenere le firme (via AST parsing)
        # Nota: controlliamo stringhe parziali per evitare problemi di formattazione spazi
        assert "def hello_world" in content
        assert "class MyClass:" in content
        
        # NON deve contenere il corpo del codice
        assert "print(\"Hello content\")" not in content
        assert "return 1" not in content

    def test_focus_mode_hybrid(self, tmp_path):
        """Testa --focus combined (ibrido)."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        # Focus solo su main.py
        result = runner.invoke(test_app, [str(tmp_path), "--focus", "main.py", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # main.py deve essere FULL
        assert "--- START OF FILE: main.py ---" in content
        assert "print(\"Hello content\")" in content
        
        # utils/helper.py NON era in focus, quindi non dovrebbe esserci il contenuto
        assert "--- START OF FILE: utils/helper.py ---" not in content

    def test_focus_with_light_background(self, tmp_path):
        """Testa --light insieme a --focus."""
        self.create_dummy_python_project(tmp_path)
        
        output_file = tmp_path / "llm_context.md"
        # Focus su main.py, ma background --light
        result = runner.invoke(test_app, [str(tmp_path), "--light", "--focus", "main.py", "-o", str(output_file)])
        
        content = output_file.read_text(encoding="utf-8")
        
        # main.py FULL
        assert "print(\"Hello content\")" in content
        
        # utils/helper.py LIGHT (deve esserci la firma)
        assert "def help_me" in content

    def test_toml_configuration(self, tmp_path):
        """Testa che .deepbase.toml venga letto e rispettato."""
        self.create_dummy_python_project(tmp_path)
        
        # Crea configurazione per ignorare "secrets.py"
        toml_file = tmp_path / ".deepbase.toml"
        toml_file.write_text('ignore_files = ["secrets.py"]', encoding="utf-8")
        
        output_file = tmp_path / "llm_context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--all", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # secrets.py NON deve apparire
        assert "secrets.py" not in content
        assert "API_KEY" not in content

    def test_custom_output_path(self, tmp_path):
        """Testa l'opzione -o per il file di output."""
        self.create_dummy_python_project(tmp_path)
        
        custom_out = tmp_path / "custom_analysis.txt"
        result = runner.invoke(test_app, [str(tmp_path), "-o", str(custom_out)])
        
        assert result.exit_code == 0
        assert custom_out.exists()
        
    def test_error_handling_invalid_path(self):
        """Testa che il programma gestisca percorsi inesistenti."""
        result = runner.invoke(test_app, ["/percorso/inesistente/assoluto"])
        assert result.exit_code == 1
        assert "Target not found" in result.stdout