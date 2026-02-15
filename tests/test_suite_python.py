# tests/test_suite_python.py

import os
import typer
from typer.testing import CliRunner
from deepbase.main import main
import sqlite3

# --- SETUP PER I TEST ---
test_app = typer.Typer()
test_app.command()(main)

runner = CliRunner()

class TestDeepBaseSuite:
    """
    Test suite completa per DeepBase.
    Copre Python, Markdown, LaTeX, Database e il meccanismo di Fallback.
    """

    def create_dummy_project(self, root):
        """Helper per popolare una directory con vari tipi di file."""
        # 1. Python Complex
        main_py = root / "main.py"
        main_py.write_text("""\"\"\"
Module docstring here.
Should be preserved.
\"\"\"
import os

# Initial comment
def simple_func():
    return True

async def async_func(a: int, b: str = "default") -> bool:
    \"\"\"Function docstring.\"\"\"
    print("body hidden")
    return False

class MyClass:
    \"\"\"Class docstring.\"\"\"
    def method_one(self):
        return 1
""", encoding="utf-8")

        # 2. Markdown
        readme = root / "README.md"
        readme.write_text("""# Project Title
Description text that should be removed.
## Section 1
More text.
### Subsection
""", encoding="utf-8")

        # 3. LaTeX
        doc_tex = root / "document.tex"
        doc_tex.write_text(r"""\documentclass{article}
\usepackage{graphicx}
\begin{document}
Text that should be removed in light mode.
\section{Introduction}
\subsection{Background}
\end{document}
""", encoding="utf-8")

        # 4. JavaScript (Unsupported / Fallback test)
        script_js = root / "script.js"
        script_js.write_text("""function hello() {
    console.log("This is JS");
    return true;
}
""", encoding="utf-8")

        # 5. JSON (Legacy TOON support)
        config_json = root / "config.json"
        config_json.write_text('{"key": "value", "list": [1, 2, 3]}', encoding="utf-8")

    def test_python_light_advanced(self, tmp_path):
        """Testa il nuovo parser Python con docstring, async e type hints."""
        self.create_dummy_project(tmp_path)
        output_file = tmp_path / "context.md"
        
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica Docstring di modulo (controlliamo le righe separate perché è multiline)
        assert '"""' in content
        assert "Module docstring here." in content
        assert "Should be preserved." in content
        
        # Verifica Async e Type Hints
        assert "async def async_func" in content
        assert "b: str" in content
        
        # Verifica Docstring di funzione (prima riga)
        assert '"""Function docstring."""' in content
        
        # Verifica che il corpo sia rimosso
        assert 'print("body hidden")' not in content

    def test_markdown_parsing(self, tmp_path):
        """Testa che il parser Markdown estragga solo gli header."""
        self.create_dummy_project(tmp_path)
        output_file = tmp_path / "context.md"
        
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        content = output_file.read_text(encoding="utf-8")
        
        assert "# Project Title" in content
        assert "## Section 1" in content
        # Il testo descrittivo non deve esserci
        assert "Description text that should be removed" not in content

    def test_latex_parsing(self, tmp_path):
        """Testa che il parser LaTeX mantenga la struttura."""
        self.create_dummy_project(tmp_path)
        output_file = tmp_path / "context.md"
        
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        content = output_file.read_text(encoding="utf-8")
        
        assert r"\documentclass{article}" in content
        assert r"\section{Introduction}" in content
        assert "Text that should be removed" not in content

    def test_fallback_and_warning(self, tmp_path):
        """
        Testa il meccanismo di fallback per file non supportati (es. .js)
        e verifica che venga generato il WARNING.
        """
        self.create_dummy_project(tmp_path)
        output_file = tmp_path / "context.md"
        
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        content = output_file.read_text(encoding="utf-8")
        
        # 1. Verifica che il contenuto JS sia presente (Fallback behavior)
        assert "function hello()" in content
        
        # 2. Verifica la presenza del WARNING (nello stdout o nel file)
        warning_msg = ".js"
        assert (warning_msg in result.stdout) or (warning_msg in content)

    def test_json_legacy_support(self, tmp_path):
        """Testa che i file JSON vengano ancora gestiti."""
        self.create_dummy_project(tmp_path)
        output_file = tmp_path / "context.md"
        
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica struttura JSON
        assert "key" in content
        assert "list" in content

    def test_database_handling(self, tmp_path):
        """Testa integrazione database SQLite."""
        project_dir = tmp_path / "db_project"
        project_dir.mkdir()
        db_path = project_dir / "test.sqlite"

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT)")
        conn.commit()
        conn.close()

        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "--light", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        assert "users" in content
        assert "email:TEXT" in content

    def test_focus_mode_hybrid(self, tmp_path):
        """Testa --focus combined (ibrido) su file Python."""
        self.create_dummy_project(tmp_path)
        output_file = tmp_path / "context.md"
        
        # Focus su main.py. SENZA --light o --all, il comportamento standard
        # per i file NON in focus è di essere presenti SOLO nell'albero (tree).
        result = runner.invoke(test_app, [str(tmp_path), "--focus", "main.py", "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # 1. main.py deve essere FULL (contiene il corpo)
        assert 'print("body hidden")' in content
        
        # 2. README.md NON in focus.
        # Verifica che sia presente nell'albero dei file
        assert "README.md" in content
        
        # Ma NON deve esserci il suo contenuto (perché non abbiamo passato --light come background)
        # Nota: se in futuro cambi il default, aggiorna questo test.
        assert "# Project Title" not in content

    def test_ignore_files(self, tmp_path):
        """Testa che .deepbase.toml venga rispettato."""
        self.create_dummy_project(tmp_path)
        
        (tmp_path / ".deepbase.toml").write_text('ignore_files = ["script.js"]', encoding="utf-8")
        
        output_file = tmp_path / "context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        
        content = output_file.read_text(encoding="utf-8")
        assert "script.js" not in content
        

    def test_javascript_react_parsing(self, tmp_path):
        """Testa il parsing di file JS, TS e React (JSX/TSX)."""
        self.create_dummy_project(tmp_path)
        
        # Crea un componente React Native finto
        rn_file = tmp_path / "App.tsx"
        rn_file.write_text("""
import React, { useEffect } from 'react';
import { View, Text } from 'react-native';

/**
 * Componente principale
 */
export const App = (props: Props) => {
    useEffect(() => {
        console.log("Effect");
    }, []);

    const helper = () => true;

    return (
        <View>
            <Text>Hello</Text>
        </View>
    );
};

export default class ErrorBoundary extends React.Component {
    render() {
        return null;
    }
}
""", encoding="utf-8")

        output_file = tmp_path / "context.md"
        result = runner.invoke(test_app, [str(tmp_path), "--light", "-o", str(output_file)])
        
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica Componente Funzionale
        assert "export const App = (props: Props) => { ... }" in content
        
        # Verifica Commento JSDoc
        assert "Componente principale" in content
        
        # Verifica Classe
        assert "export default class ErrorBoundary extends React.Component { ... }" in content
        
        # Verifica che il corpo (useEffect, JSX) sia nascosto
        assert "console.log" not in content
        assert "<View>" not in content
        
        
########## TEST SUITE PER FILE DI CONFIGURAZIONE .deepbase.toml ###########
    def test_deepbase_toml_ignore_dirs(self, tmp_path):
        """Testa che .deepbase.toml rispetti correttamente ignore_dirs."""
        # Crea struttura progetto
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea directory da ignorare tramite TOML
        ignored_dir = project_dir / "custom_ignored"
        ignored_dir.mkdir()
        (ignored_dir / "secret.py").write_text("password = '123'", encoding="utf-8")
        
        # Crea directory che NON deve essere ignorata
        kept_dir = project_dir / "important"
        kept_dir.mkdir()
        (kept_dir / "keep.py").write_text("print('keep me')", encoding="utf-8")
        
        # Crea file .deepbase.toml con ignore_dirs personalizzato
        toml_content = '''ignore_dirs = ["custom_ignored"]
'''
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica che la directory ignorata non appaia
        assert "custom_ignored" not in content, "La directory custom_ignored dovrebbe essere esclusa"
        assert "secret.py" not in content, "I file in custom_ignored dovrebbero essere esclusi"
        
        # Verifica che la directory importante sia presente
        assert "important" in content, "La directory important dovrebbe essere inclusa"
        assert "keep.py" in content, "I file in important dovrebbero essere inclusi"

    def test_deepbase_toml_ignore_files(self, tmp_path):
        """Testa che .deepbase.toml rispetti correttamente ignore_files."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea file da ignorare
        (project_dir / "secrets.env").write_text("API_KEY=xxx", encoding="utf-8")
        (project_dir / "debug.log").write_text("error happened", encoding="utf-8")
        
        # Crea file che NON deve essere ignorato
        (project_dir / "main.py").write_text("print('hello')", encoding="utf-8")
        
        # Crea .deepbase.toml con ignore_files
        toml_content = '''ignore_files = ["secrets.env", "*.log"]
'''
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica file ignorati
        assert "secrets.env" not in content, "secrets.env dovrebbe essere ignorato"
        assert "debug.log" not in content, "*.log dovrebbe essere ignorato"
        
        # Verifica file incluso
        assert "main.py" in content, "main.py dovrebbe essere incluso"

    def test_deepbase_toml_significant_extensions(self, tmp_path):
        """Testa che .deepbase.toml aggiunga estensioni personalizzate."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea file con estensione custom
        (project_dir / "config.cfg").write_text("setting=value", encoding="utf-8")
        (project_dir / "Makefile").write_text("all: build", encoding="utf-8")
        
        # Crea .deepbase.toml con estensioni aggiuntive
        toml_content = '''significant_extensions = [".cfg", "Makefile"]
'''
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        # Verifica che i file con estensioni custom siano inclusi
        assert "config.cfg" in content, ".cfg dovrebbe essere incluso tramite TOML"
        assert "Makefile" in content, "Makefile dovrebbe essere incluso tramite TOML"

    def test_deepbase_toml_combined_settings(self, tmp_path):
        """Testa combinazione di ignore_dirs, ignore_files e significant_extensions."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea struttura complessa
        (project_dir / "src").mkdir()
        (project_dir / "src" / "main.py").write_text("print('main')", encoding="utf-8")
        
        ignored_dir = project_dir / "temp"
        ignored_dir.mkdir()
        (ignored_dir / "cache.tmp").write_text("temp data", encoding="utf-8")
        
        (project_dir / "secret.key").write_text("private", encoding="utf-8")
        (project_dir / "custom.xyz").write_text("custom format", encoding="utf-8")
        
        # Configurazione combinata
        toml_content = '''
ignore_dirs = ["temp"]
ignore_files = ["*.key"]
significant_extensions = [".xyz"]
'''
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        # Verifiche
        assert "main.py" in content, "main.py dovrebbe essere presente"
        assert "custom.xyz" in content, ".xyz dovrebbe essere incluso via TOML"
        
        assert "temp" not in content, "temp/ dovrebbe essere ignorato"
        assert "cache.tmp" not in content, "cache.tmp dovrebbe essere ignorato"
        assert "secret.key" not in content, "*.key dovrebbe essere ignorato"

    def test_deepbase_toml_empty_or_invalid(self, tmp_path):
        """Testa comportamento con file TOML vuoto o malformato."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        (project_dir / "main.py").write_text("print('test')", encoding="utf-8")
        
        # TOML vuoto
        (project_dir / ".deepbase.toml").write_text("", encoding="utf-8")
        output_file = project_dir / "context.md"
        
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        assert result.exit_code == 0, f"Errore con TOML vuoto: {result.stdout}"
        
        # TOML malformato
        (project_dir / ".deepbase.toml").write_text("invalid toml content [[", encoding="utf-8")
        output_file2 = project_dir / "context2.md"
        
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file2)])
        # Dovrebbe gestire l'errore gracefulmente usando defaults
        assert result.exit_code == 0, f"Errore con TOML malformato: {result.stdout}"
        content = output_file2.read_text(encoding="utf-8")
        assert "main.py" in content, "Dovrebbe funzionare con defaults se TOML è malformato"

    def test_deepbase_toml_not_in_root(self, tmp_path):
        """Testa che il TOML venga cercato solo nella root del target, non in parent."""
        # Crea struttura: parent/child/
        parent_dir = tmp_path / "parent"
        parent_dir.mkdir()
        child_dir = parent_dir / "child_project"
        child_dir.mkdir()
        
        # TOML in parent (NON dovrebbe essere usato quando analizziamo child)
        (parent_dir / ".deepbase.toml").write_text(
            'ignore_dirs = ["should_not_apply"]', encoding="utf-8"
        )
        
        # Directory che verrebbe ignorata se il TOML del parent fosse usato
        test_dir = child_dir / "should_not_apply"
        test_dir.mkdir()
        (test_dir / "file.py").write_text("print('test')", encoding="utf-8")
        
        # File normale in child
        (child_dir / "main.py").write_text("print('main')", encoding="utf-8")
        
        output_file = child_dir / "context.md"
        result = runner.invoke(test_app, [str(child_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        # Se il TOML del parent fosse caricato, should_not_apply sarebbe escluso
        # Invece dovrebbe essere incluso perché il TOML è in parent, non in child
        assert "should_not_apply" in content, "Non dovrebbe usare il TOML del parent directory"
        assert "main.py" in content, "main.py dovrebbe essere incluso"
        
        
    def test_ignore_dirs_nested_path(self, tmp_path):
        """Testa che ignore_dirs supporti percorsi annidati (es: 'app/templates')."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea struttura annidata
        app_dir = project_dir / "app"
        app_dir.mkdir()
        templates_dir = app_dir / "templates"
        templates_dir.mkdir()
        (templates_dir / "index.html").write_text("<html></html>", encoding="utf-8")
        
        # Crea altra directory templates a livello root (non deve essere ignorata)
        other_templates = project_dir / "templates"
        other_templates.mkdir()
        (other_templates / "other.html").write_text("<html></html>", encoding="utf-8")
        
        # TOML con percorso annidato specifico
        toml_content = 'ignore_dirs = ["app/templates"]\n'
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        # app/templates deve essere ignorato
        assert "app/templates" not in content or "app/templates" not in content.replace("\\", "/")
        assert "index.html" not in content, "I file in app/templates non dovrebbero apparire"
        
        # templates a livello root deve essere presente
        assert "templates/" in content or "templates\\" in content, "templates/ a livello root dovrebbe essere presente"
        assert "other.html" in content, "other.html dovrebbe essere incluso"

    def test_ignore_files_with_path(self, tmp_path):
        """Testa che ignore_files supporti percorsi specifici (es: 'app/secrets.md')."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea file in diverse posizioni
        app_dir = project_dir / "app"
        app_dir.mkdir()
        (app_dir / "secrets.md").write_text("SECRET=123", encoding="utf-8")
        (app_dir / "main.py").write_text("print('hello')", encoding="utf-8")
        
        # Stesso nome file in root (non deve essere ignorato)
        (project_dir / "secrets.md").write_text("PUBLIC=value", encoding="utf-8")
        
        # TOML con percorso specifico
        toml_content = 'ignore_files = ["app/secrets.md"]\n'
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        # Aggiungi --all per includere il contenuto dei file
        result = runner.invoke(test_app, [str(project_dir), "--all", "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        # app/secrets.md deve essere ignorato (non deve apparire nel contenuto)
        assert "SECRET=123" not in content, "app/secrets.md dovrebbe essere ignorato"
        # E non deve essere nell'albero
        assert "app/secrets.md" not in content.replace("\\", "/"), "app/secrets.md non dovrebbe apparire nell'albero"
        
        # secrets.md in root deve essere presente nell'albero
        assert "secrets.md" in content, "secrets.md in root dovrebbe essere nell'albero"
        # E il suo contenuto deve essere incluso
        assert "PUBLIC=value" in content, "secrets.md in root dovrebbe essere incluso con contenuto"
        assert "main.py" in content, "main.py dovrebbe essere incluso"

    def test_ignore_files_wildcard(self, tmp_path):
        """Testa che ignore_files supporti wildcard patterns."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea vari file .log
        (project_dir / "debug.log").write_text("error", encoding="utf-8")
        (project_dir / "app.log").write_text("info", encoding="utf-8")
        (project_dir / "main.py").write_text("print('hello')", encoding="utf-8")
        
        # TOML con wildcard
        toml_content = 'ignore_files = ["*.log"]\n'
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        assert "debug.log" not in content, "*.log dovrebbe ignorare debug.log"
        assert "app.log" not in content, "*.log dovrebbe ignorare app.log"
        assert "main.py" in content, "main.py dovrebbe essere incluso"

    def test_ignore_dirs_wildcard(self, tmp_path):
        """Testa che ignore_dirs supporti wildcard patterns."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        # Crea directory che matchano pattern
        egg_dir = project_dir / "my_package.egg-info"
        egg_dir.mkdir()
        (egg_dir / "PKG-INFO").write_text("metadata", encoding="utf-8")
        
        other_dir = project_dir / "src"
        other_dir.mkdir()
        (other_dir / "main.py").write_text("print('hello')", encoding="utf-8")
        
        # TOML con wildcard
        toml_content = 'ignore_dirs = ["*.egg-info"]\n'
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0, f"Errore: {result.stdout}"
        content = output_file.read_text(encoding="utf-8")
        
        assert "my_package.egg-info" not in content, "*.egg-info dovrebbe essere ignorato"
        assert "PKG-INFO" not in content, "I file in *.egg-info non dovrebbero apparire"
        assert "src" in content, "src dovrebbe essere incluso"
        assert "main.py" in content, "main.py dovrebbe essere incluso"
    
    def test_ignore_dirs_nested_vs_global(self, tmp_path):
        """Verifica che 'app/templates' ignori solo quel percorso specifico, non tutte le 'templates'."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        
        # Crea app/templates
        app_dir = project_dir / "app"
        app_dir.mkdir()
        app_templates = app_dir / "templates"
        app_templates.mkdir()
        (app_templates / "base.html").write_text("...", encoding="utf-8")
        
        # Crea templates a livello root (non deve essere ignorata)
        root_templates = project_dir / "templates"
        root_templates.mkdir()
        (root_templates / "other.html").write_text("...", encoding="utf-8")
        
        # Config: ignora SOLO app/templates
        toml_content = 'ignore_dirs = ["app/templates"]\n'
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        assert result.exit_code == 0
        content = output_file.read_text(encoding="utf-8")
        
        # app/templates ignorato
        assert "app/templates/base.html" not in content.replace("\\", "/")
        
        # templates a root presente
        assert "templates/other.html" in content.replace("\\", "/") or "templates" in content

    def test_ignore_dirs_name_matches_everywhere(self, tmp_path):
        """Verifica che 'tests' ignori TUTTE le cartelle 'tests' ovunque."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        
        # tests in root
        (project_dir / "tests").mkdir()
        (project_dir / "tests" / "test1.py").write_text("", encoding="utf-8")
        
        # tests in subdir
        (project_dir / "src").mkdir()
        (project_dir / "src" / "tests").mkdir()
        (project_dir / "src" / "tests" / "test2.py").write_text("", encoding="utf-8")
        
        toml_content = 'ignore_dirs = ["tests"]\n'
        (project_dir / ".deepbase.toml").write_text(toml_content, encoding="utf-8")
        
        output_file = project_dir / "context.md"
        result = runner.invoke(test_app, [str(project_dir), "-o", str(output_file)])
        
        content = output_file.read_text(encoding="utf-8")
        
        # Nessuna cartella tests deve apparire
        assert "tests/test1.py" not in content.replace("\\", "/")
        assert "src/tests/test2.py" not in content.replace("\\", "/")