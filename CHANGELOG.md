feat: add SQLite database schema extraction support (#1)

- Add new database.py module with complete schema introspection
- Support .db, .sqlite, .sqlite3 extensions and magic bytes detection
- Implement three context modes: full schema, TOON (minimal), hybrid focus
- Add table-level focusing via 'database.db/tablename' syntax
- Include foreign keys, indexes, constraints and row counts in output
- Update parsers.py and toon.py to handle database files
- Add database icons (🗄️) in directory tree visualization
- Maintain backward compatibility with existing flags (--all, --toon, --focus)

BREAKING CHANGE: None