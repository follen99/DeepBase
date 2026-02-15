# Esempi pratici

Questa pagina contiene esempi reali d'uso di DeepBase per diversi scenari e tipologie di progetto.

---

## 📁 Esempio 1: Progetto Python Flask

**Struttura progetto:**
```
my-flask-app/
├── app/
│   ├── __init__.py
│   ├── routes.py          # <- focus qui
│   ├── models.py          # <- focus qui
│   ├── forms.py
│   ├── templates/         # <- da ignorare
│   └── static/
├── config.py
├── requirements.txt
├── tests/                   # <- da ignorare
└── instance/
    └── app.db               # <- database
```

**Configurazione `.deepbase.toml`:**
```toml
ignore_dirs = ["app/templates", "tests", "instance", "__pycache__"]
ignore_files = ["*.pyc", ".env", ".flaskenv"]
```

**Comando:**
```bash
deepbase . --light --focus "app/routes.py" --focus "app/models.py"
```

**Output:** Struttura light dell'intero progetto + contenuto completo di routes e models.

---

## 📁 Esempio 2: Progetto React + Node.js

**Struttura progetto:**
```
my-react-app/
├── src/
│   ├── components/
│   │   ├── Button.jsx
│   │   └── Card.jsx
│   ├── pages/
│   │   ├── Home.jsx       # <- focus qui
│   │   └── Dashboard.jsx  # <- focus qui
│   └── utils/
│       └── api.js
├── public/
├── node_modules/            # <- da ignorare
├── build/                   # <- da ignorare
├── package.json
└── package-lock.json        # <- da ignorare
```

**Configurazione `.deepbase.toml`:**
```toml
ignore_dirs = ["node_modules", "build", "dist", "coverage", ".next"]
ignore_files = ["package-lock.json", "yarn.lock", "*.log"]
```

**Comando:**
```bash
deepbase . --light --focus "src/pages/*"
```

---

## 📁 Esempio 3: Analisi Database SQLite

**Scenario:** Vuoi documentare lo schema del database + alcune query importanti.

**Struttura:**
```
data-project/
├── migrations/
│   ├── 001_initial.sql    # <- focus qui
│   └── 002_add_users.sql  # <- focus qui
├── queries/
│   ├── reports.sql        # <- focus qui
│   └── analytics.sql
└── production.db          # <- database da analizzare
```

**Configurazione `.deepbase.toml`:**
```toml
ignore_dirs = ["backups", "temp"]
significant_extensions = [".sql", ".db", ".sqlite"]
```

**Comando:**
```bash
deepbase . --light --focus "production.db" --focus "migrations/*" --focus "queries/reports.sql"
```

**Output:** Schema completo del database + contenuto SQL dei file focalizzati.

---

## 📁 Esempio 4: Monorepo con più package

**Struttura:**
```
monorepo/
├── packages/
│   ├── core/
│   │   ├── src/
│   │   └── package.json
│   ├── ui/                  # <- focus solo questo
│   │   ├── src/
│   │   └── package.json
│   └── utils/
│       └── src/
├── apps/
│   ├── web/
│   └── admin/
└── turbo.json
```

**Comando:**
```bash
deepbase . --light --focus "packages/ui/**/*"
```

---

## 📁 Esempio 5: Documentazione LaTeX

**Struttura:**
```
thesis/
├── chapters/
│   ├── introduction.tex
│   ├── methods.tex          # <- focus qui
│   ├── results.tex          # <- focus qui
│   └── conclusion.tex
├── figures/
├── bibliography.bib
└── main.tex
```

**Comando:**
```bash
deepbase . --light --focus "chapters/methods.tex" --focus "chapters/results.tex"
```

---

## 📁 Esempio 6: Configurazione granulare (esclusioni complesse)

**Scenario:** Progetto con molti file temporanei e configurazioni locali.

**`.deepbase.toml`:**
```toml
# Directory
ignore_dirs = [
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    "coverage",
    ".tox",
    # Esclusioni specifiche per percorso
    "legacy/old_components",      # solo questa specifica
    "experiments/temp_*",         # tutte le cartelle temp_*
    "src/components/__dev__"      # cartella dev interna
]

# File
ignore_files = [
    "*.log",
    "*.tmp",
    "*.bak",
    ".env*",
    "local.settings.json",
    "secrets.*",
    # Esclusioni specifiche per percorso
    "config/local.yaml",
    "src/debug_utils.py"
]

# Estensioni extra
significant_extensions = [".prisma", ".graphql", ".proto"]
```

**Comando:**
```bash
deepbase . --light
```

---

## 📁 Esempio 7: Focus da file esterno

**Scenario:** Hai una lista lunga di file da analizzare.

**File `focus-list.txt`:**
```
src/auth/login.js
src/auth/register.js
src/middleware/jwt.js
config/auth.yaml
tests/auth.test.js
```

**Comando:**
```bash
deepbase . --light --focus-file focus-list.txt
```

---

## 📁 Esempio 8: CI/CD - Generazione automatica contesto

**Scenario:** Generare contesto per PR review automatica.

**Script `.github/workflows/context.yml`:**
```yaml
name: Generate LLM Context

on:
  pull_request:
    paths:
      - 'src/**'

jobs:
  context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install DeepBase
        run: pip install deepbase
        
      - name: Generate context
        run: |
          deepbase . --light --focus "src/**" -o pr-context.md
          
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: llm-context
          path: pr-context.md
```

---

## 📁 Esempio 9: Confronto tra versioni

**Scenario:** Hai due branch e vuoi confrontare le differenze di struttura.

```bash
# Branch main
git checkout main
deepbase . --light -o context-main.md

# Branch feature
git checkout feature-branch
deepbase . --light -o context-feature.md

# Ora confronta i due file con diff o LLM
diff context-main.md context-feature.md
```

---

## 📁 Esempio 10: Progetto complesso multi-linguaggio

**Struttura:**
```
fullstack-app/
├── backend/
│   ├── src/
│   │   ├── controllers/     # Python
│   │   ├── models/          # Python
│   │   └── main.py
│   ├── migrations/          # SQL
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React/TS
│   │   └── pages/
│   └── package.json
├── mobile/
│   └── ios/                 # <- da ignorare (build)
├── shared/
│   └── types.ts             # <- focus qui (tipi condivisi)
└── README.md
```

**`.deepbase.toml`:**
```toml
ignore_dirs = [
    "backend/__pycache__",
    "frontend/node_modules",
    "mobile/ios",
    "mobile/android",
    "mobile/build"
]

ignore_files = [
    "frontend/package-lock.json",
    "backend/*.pyc"
]
```

**Comando:**
```bash
deepbase . --light --focus "backend/src/main.py" --focus "shared/types.ts"
```

---

## 💡 Tips & Tricks

### Verifica cosa verrà incluso

```bash
# Genera solo struttura (veloce, per controllare)
deepbase . > structure.md

# Poi aggiungi --light o --all quando sei soddisfatto
```

### Stima token prima di generare

Guarda la stima nell'output dell'albero:
```
📁 my-project/ (245.6 KB | ~61.4k t)
```

Se troppo alto, aumenta le esclusioni nel TOML.

### Ignorare file già nel contesto

DeepBase ignora automaticamente l'output file (`llm_context.md` di default) per evitare loop.

### Usa con pipe

```bash
deepbase . --light | head -n 100  # prime 100 righe
deepbase . --light | wc -l        # conta righe
```

---

Hai un caso d'uso particolare? [Apri una issue](https://github.com/follen99/deepbase/issues) per aggiungerlo agli esempi!