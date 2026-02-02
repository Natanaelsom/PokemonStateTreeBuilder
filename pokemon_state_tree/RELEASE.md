# Automated release

Use `release.ps1` to build the project, commit the generated executable and push to `origin/main`.

Usage (PowerShell):

```powershell
.
elease.ps1        # Will abort if working tree is not clean
.
elease.ps1 -Force # Force even with uncommitted changes
```

The script will:
- run `build_executable.py` using `.venv\Scripts\python.exe` if available
- ensure `Executavel/PokemonStateTreeBuilder.exe` exists
- stage and commit the `.exe` with a message including the `version.py` value
- push to `origin/main`
