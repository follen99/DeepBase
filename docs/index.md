# DeepBase

**DeepBase** è un tool CLI che analizza una directory di progetto, estrae la struttura delle cartelle e il contenuto dei file di codice significativi, consolidandoli in un unico file di contesto per LLM.

## Versione corrente: 1.8.1

---

## 🚀 Quick Start

```bash
pip install deepbase

# Analisi base (struttura solo)
deepbase /path/to/project

# Modalità Light (risparmio token)
deepbase /path/to/project --light

# Contenuto completo
deepbase /path/to/project --all

# Focus su file specifici
deepbase /path/to/project --light --focus "src/main.py" --focus "config.yaml"
```

---

## 📖 Documentazione completa

- [Installazione](#installazione)
- [Modalità di funzionamento](#modalità)
- [Configurazione `.deepbase.toml`](#configurazione)
- [Database SQLite](#database)
- [Parser e linguaggi supportati](#parser)
- [API Reference](./reference.md)

---

## Installazione

### Come installare DeepBase

```bash
pip install deepbase
```

### Modalità di sviluppo

```bash
git clone https://github.com/follen99/deepbase.git
cd deepbase
pip install -e ".[dev]"
```

---

## Modalità di funzionamento

### Default (Struttura solo)
Genera solo l'albero delle directory, senza contenuto dei file.

```bash
deepbase .
```

### `--all` - Contenuto completo
Include il contenuto completo di tutti i file significativi.

⚠️ Usare solo per progetti piccoli (rischio di file troppo grandi per gli LLM).

```bash
deepbase . --all
```

### `--light` - Modalità Light (consigliata)
Estrae solo le "firme" semantiche: classi, funzioni, docstring, commenti iniziali.
Risparmia fino al 90% dei token mantenendo la comprensione dell'architettura.

```bash
deepbase . --light
```

### `--focus` - Hybrid Mode
Combina Light mode per l'intero progetto con contenuto completo per file specifici.

```bash
# Via CLI
deepbase . --light --focus "server/controllers/*" --focus "client/src/login.js"

# Via file
deepbase . --light --focus-file context_task.txt
```

---

## Configurazione

Crea un file `.deepbase.toml` nella root del progetto:

```toml
# Directory da ignorare (nomi, percorsi relativi, wildcard)
ignore_dirs = [
    "node_modules",           # ignora ovunque
    "app/templates",          # ignora solo app/templates
    "*.egg-info",             # ignora tutte le cartelle .egg-info
    "temp_*"                  # ignora temp_1, temp_2, etc.
]

# File da ignorare (nomi, percorsi, wildcard)
ignore_files = [
    "*.log",                  # tutti i file .log
    "secrets.env",            # file specifico
    "app/config.local.py",    # percorso specifico
    ".env*"                   # .env, .env.local, etc.
]

# Estensioni aggiuntive da includere
significant_extensions = [".cfg", "Makefile", ".prisma"]
```

### Pattern di esclusione

| Pattern | Esempio | Comportamento |
|---------|---------|---------------|
| Nome semplice | `"tests"` | Ignora TUTTE le cartelle/file chiamati "tests" a qualsiasi livello |
| Percorso relativo | `"app/templates"` | Ignora SOLO la cartella templates dentro app |
| Wildcard | `"*.egg-info"` | Ignora tutti i match del pattern |

---

## Database

DeepBase supporta l'analisi di database SQLite:

```bash
# Schema completo
deepbase database.db --all

# Schema light (solo struttura)
deepbase database.db --light

# Focus su tabelle specifiche
deepbase database.db --light --focus "users" --focus "orders"
```

---

## Parser

Supporto nativo per:

| Linguaggio | Estensioni | Modalità Light |
|------------|-----------|----------------|
| Python | `.py` | ✅ Firme, type hints, docstring |
| JavaScript/TypeScript | `.js`, `.jsx`, `.ts`, `.tsx` | ✅ Funzioni, classi, componenti React |
| Markdown | `.md`, `.markdown` | ✅ Headers, struttura |
| LaTeX | `.tex`, `.sty`, `.cls` | ✅ Sezioni, comandi |
| JSON | `.json` | ✅ Struttura dati |
| SQLite | `.db`, `.sqlite` | ✅ Schema, tabelle, relazioni |
| Altri | `*` | ⚠️ Fallback (prime 10 righe) |

---

## Esempi

### Esempio 1: Progetto Python Flask

```bash
cd my-flask-app
deepbase . --light --focus "app/routes.py" --focus "app/models.py"
```

### Esempio 2: Progetto React

```toml
# .deepbase.toml
ignore_dirs = ["node_modules", "build", "dist", "coverage"]
ignore_files = ["package-lock.json", "*.log"]
```

```bash
deepbase . --light
```

### Esempio 3: Analisi database + codice

```bash
deepbase . --light --focus "instance/app.db"
```

---

## Troubleshooting

### Il file `.deepbase.toml` non viene rilevato

Verifica che:
1. Il file sia nella **root del progetto da analizzare**, non della directory corrente
2. Il nome sia esatto: `.deepbase.toml` (con il punto iniziale)
3. I permessi siano corretti: `ls -la .deepbase.toml`

### File troppo grande per l'LLM

Usa `--light` o aumenta gli esclusioni nel TOML.

---

## Contributing

Issue e PR su [GitHub](https://github.com/follen99/deepbase).

---

## License

GPL 3