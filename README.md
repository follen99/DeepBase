# DeepBase

<p align="center">
  <img src="https://img.shields.io/badge/version-1.8.0-blue?style=for-the-badge&logo=github" alt="Version 1.8.0">
  <img src="https://img.shields.io/badge/python-3.8+-brightgreen?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-GPL%203-purple?style=for-the-badge" alt="GPL 3 License">
  <img src="https://img.shields.io/badge/pypi-ready-orange?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI Ready">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/🧠%20LLM-Ready-ff6b6b?style=flat-square" alt="LLM Ready">
  <img src="https://img.shields.io/badge/⚡%20TOON-Optimized-4ecdc4?style=flat-square" alt="TOON Optimized">
  <img src="https://img.shields.io/badge/🔍%20Smart%20Parsing-45b7d1?style=flat-square" alt="Smart Parsing">
</p>

<p align="center">
  <b>DeepBase</b> è un tool CLI che analizza una directory di progetto, estrae la struttura delle cartelle e il contenuto dei file di codice significativi, consolidandoli in un unico file di contesto per LLM.
</p>

---

## ✨ Features

| Feature | Descrizione |
|---------|-------------|
| 📁 **Project Structure** | Genera una tree view della struttura di cartelle e file |
| 🧠 **Smart Filtering** | Ignora automaticamente directory comuni (`.git`, `venv`, `node_modules`) |
| ⚡ **Token Optimization (TOON)** | Genera "Semantic Skeletons" (classi, firme, docstring) per risparmiare fino al 90% dei token |
| 💡 **Light Mode** | Modalità ultra-leggera con solo firme di metodi e commenti iniziali |
| 🔍 **Hybrid Focus Mode** | Combina contesto leggero per l'intero progetto con contenuto completo per file/folder specifici |
| 🗄️ **Database Support** | Estrae schema da database SQLite (tabelle, colonne, relazioni) |
| 🌐 **Multi-Language Parsing** | Supporto nativo per Python, JavaScript, TypeScript, React (JSX/TSX), Markdown, LaTeX |
| 🔧 **Plugin System** | Architettura a plugin per parser personalizzati |
| ⚙️ **Configurable** | Personalizza via file `.deepbase.toml` |
| 📄 **Unified Output** | Tutto in un unico file, facile da copiare e incollare per gli LLM |

---

## 🚀 Installation

```sh
pip install deepbase
```

### Development Mode

```sh
git clone https://github.com/follen99/deepbase.git
cd deepbase
pip install -e ".[dev]"
```

---

## 📖 How to Use

### 1. Basic Project Analysis

**Structure Only (Default)**

Genera rapidamente una tree view della struttura del progetto:

```sh
deepbase .
```

**Include All Content**

Per generare il contesto completo con tutto il codice:

```sh
deepbase . --all
```
⚠️ *Attenzione: usare solo per progetti piccoli.*

---

### 2. Smart Token Optimization (TOON)

Per progetti grandi, inviare tutto il codice a un LLM è costoso. **TOON** estrae solo lo "scheletro" semantico:

```sh
deepbase . --toon
# oppure
deepbase . -t
```

**Risultato:** Gli LLM capiscono l'architettura usando token minimi.

---

### 3. Light Mode (Ultra-Lightweight)

Modalità ancora più leggera di TOON, include solo firme di metodi/funzioni e commenti iniziali:

```sh
deepbase . --light
# oppure
deepbase . -l
```

---

### 4. Hybrid Mode (Focus)

Combina TOON per l'intero progetto con contenuto completo per file specifici.

**Focus via CLI:**

```sh
deepbase . --toon --focus "server/controllers/*" --focus "client/src/login.js"
```

**Focus via File:**

Crea un file (es. `context_task.txt`):

```text
server/routes/auth.js
server/models/User.js
client/src/components/LoginForm.jsx
```

Esegui:

```sh
deepbase . --toon --focus-file context_task.txt
```

---

### 5. Database Analysis

DeepBase può analizzare database SQLite estraendo schema e relazioni:

```sh
# Schema completo
deepbase database.db --all

# Schema in modalità TOON (solo struttura)
deepbase database.db --toon

# Focus su tabelle specifiche
deepbase database.db --toon --focus "users" --focus "orders"
```

---

### 6. Single File Analysis

Analisi di un singolo file:

```sh
# Solo struttura (default)
deepbase README.md

# Struttura + contenuto completo
deepbase README.md --all

# Modalità TOON
deepbase script.py --toon
```

---

## 🌐 Supported Languages

| Linguaggio | Estensioni | Parser |
|------------|------------|--------|
| Python | `.py` | ✅ Nativo - Classi, funzioni, async, type hints, docstring |
| JavaScript | `.js`, `.jsx` | ✅ Nativo - Funzioni, classi, componenti React |
| TypeScript | `.ts`, `.tsx` | ✅ Nativo - Tipi, interfacce, generics |
| Markdown | `.md` | ✅ Nativo - Headers, struttura documento |
| LaTeX | `.tex` | ✅ Nativo - Sezioni, comandi |
| JSON | `.json` | ✅ Legacy - Struttura dati |
| SQLite | `.db`, `.sqlite` | ✅ Database - Schema, tabelle, colonne |
| Altri | `*` | ⚠️ Fallback - Prime 10 righe + warning |

---

## ⚙️ Configuration (.deepbase.toml)

Crea un file `.deepbase.toml` nella root del progetto:

```toml
# Directory aggiuntive da ignorare
ignore_dirs = ["my_assets", "experimental", "logs"]

# Estensioni/filename aggiuntivi da includere
significant_extensions = [".cfg", "Makefile", ".tsx", ".prisma"]

# Directory sempre incluse (anche se matchano ignore_dirs)
force_include_dirs = ["important_logs"]
```

---

## 📊 Output Example

```markdown
# Project Context: MyProject

> Total Size (raw): 15.28 KB | Est. Tokens (light): ~3,912

📁 MyProject/
├── 📄 README.md (1.9% | ~73t)
├── 📁 src/ (65.0% | ~2.5k t)
│   ├── 📄 main.py (25.0% | ~980t)
│   └── 📄 utils.py (40.0% | ~1.5k t)
└── 📁 tests/ (33.1% | ~1.3k t)
    └── 📄 test_main.py (33.1% | ~1.3k t)

### FILE CONTENTS (LIGHT — signatures only)

> FILE: src/main.py

def main() -> None: ...
class Application:
    def __init__(self, config: dict): ...
    def run(self) -> int: ...
```

---

## 🛠️ Development Workflow

```sh
# Install in editable mode
pip install -e ".[dev]"

# Run tests
pytest

# Run specific test
pytest tests/test_suite_python.py -v
```

---

## 📚 Documentation

La documentazione completa è disponibile su [GitHub Pages](https://follen99.github.io/deepbase/):

- [Getting Started](https://follen99.github.io/deepbase/)
- [API Reference](https://follen99.github.io/deepbase/reference/)
- [Examples](https://github.com/follen99/deepbase/tree/main/examples)

---

## 📝 Changelog

### [1.8.0] - 2024-02-12
- ✅ Parser JavaScript/TypeScript/React (JSX/TSX)
- ✅ Parser Markdown e LaTeX
- ✅ Supporto database SQLite
- ✅ Sistema plugin per parser
- ✅ Modalità Light avanzata
- ✅ Focus mode per tabelle database

### [1.7.0] - 2024-02-10
- ✅ Miglioramenti al parser Python (async, type hints)
- ✅ Supporto file focus da file esterno
- ✅ Stima token più accurata

---

## 🤝 Contributing

Contributi sono benvenuti! Per favore:

1. Fork il repository
2. Crea un branch (`git checkout -b feature/amazing-feature`)
3. Commit le modifiche (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

---

## 📄 License

Questo progetto è rilasciato sotto licenza **GPL 3**. Vedi il file `LICENSE` per i dettagli.

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/follen99">Giuliano Ranauro</a></sub>
</p>

<p align="center">
  <a href="https://github.com/follen99/deepbase/stargazers">⭐ Star this repo</a> •
  <a href="https://github.com/follen99/deepbase/issues">🐛 Report bug</a> •
  <a href="https://pypi.org/project/deepbase/">📦 PyPI</a>
</p>
