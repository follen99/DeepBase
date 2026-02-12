# tests/test_suite_python.py

import os
import typer
from typer.testing import CliRunner
from deepbase.main import main
import sqlite3

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
        
    def test_database_handling(self, tmp_path):
        """Testa il supporto per database SQLite (schema extraction e light mode)."""
        import sqlite3  # Import necessario qui o in cima al file

        # Creiamo una cartella e un DB reale
        project_dir = tmp_path / "db_project"
        project_dir.mkdir()
        db_path = project_dir / "test_db.sqlite"

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL)")
        cursor.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT)")
        conn.commit()
        conn.close()

        output_file = project_dir / "context.md"

        # 1. Test Full Mode (--all) -> Deve mostrare schema dettagliato
        result = runner.invoke(test_app, [str(project_dir), "--all", "-o", str(output_file)])
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")

        # Verifica che il DB sia stato processato
        assert "test_db.sqlite" in content
        
        # Verifica il contenuto generato da generate_database_context_full
        # Nota: "DATABASE SCHEMA" appare solo in single-file mode, qui cerchiamo il contenuto reale
        assert "Table: `users`" in content
        # Verifica parziale di una colonna per assicurarsi che lo schema sia stato letto
        assert "username" in content
        assert "TEXT" in content

        # 2. Test Light Mode (--light) -> Deve mostrare schema compatto (TOON)
        result = runner.invoke(test_app, [str(project_dir), "--light", "-o", str(output_file)])
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica firma compatta (TOON)
        # Cerca la definizione della tabella users e la colonna id
        assert "users" in content
        # Verifica formato TOON: nome:tipo
        assert "id:INTEGER" in content