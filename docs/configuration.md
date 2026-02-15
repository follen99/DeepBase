
# Configurazione avanzata

## File `.deepbase.toml`

Posizionare nella root del progetto da analizzare il file `.deepbase.toml`, verrà riconosciuto automaticamente.

### Esempio di file
```
# Esempio di file di configurazione per DeepBase.
# Salva questo file come .deepbase.toml nella root del tuo progetto.

# Aggiungi altre directory da ignorare.
# Queste si sommeranno a quelle di default.
 ignore_dirs = [
   "my_secret_folder",
   "temp_data"
 ]

# Aggiungi altri files da ignorare.
# Questi si sommeranno a quelle di default.
 ignore_files = [
   "secrets.txt"
 ]

# Aggiungi altre estensioni o nomi di file da includere.
 significant_extensions = [
   ".env.example",
   ".customtext"
 ]
```