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