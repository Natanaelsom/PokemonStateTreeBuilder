Param(
    [switch]$Force
)

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Host "Starting automated release (build → commit → push)"

# Determine python executable (prefer virtualenv)
$venvPy = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPy) {
    $python = $venvPy
} else {
    $python = "python"
}

# Ensure git working tree is clean unless forced
$status = git status --porcelain
if ($status -ne "" -and -not $Force) {
    Write-Error "Git working tree is not clean. Commit or run with -Force to continue."
    exit 1
}

Write-Host "Running build_executable.py with: $python"
& $python .\build_executable.py

if (-not (Test-Path ".\Executavel\PokemonStateTreeBuilder.exe")) {
    Write-Error "Build failed: Executable not found at .\Executavel\PokemonStateTreeBuilder.exe"
    exit 1
}

# Read version from version.py if available (safe parse)
$version = "unknown"
if (Test-Path ".\version.py") {
    foreach ($line in Get-Content .\version.py) {
        if ($line -match 'VERSION') {
            $parts = $line -split '='
            if ($parts.Length -ge 2) {
                $val = $parts[1].Trim()
                    # remove surrounding quotes if present (use -replace to avoid char overload issues)
                    $val = $val -replace "'", ''
                    $val = $val -replace '"', ''
                if ($val) { $version = $val; break }
            }
        }
    }
}

Write-Host "Staging executable..."
git add Executavel/PokemonStateTreeBuilder.exe

Write-Host "Committing release (version $version)..."
git commit -m "Release v$version - automated build $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -q 2>$null
if ($LASTEXITCODE -eq 0) { Write-Host "Committed." } else { Write-Host "No changes to commit." }

Write-Host "Pushing to origin/main..."
git push origin main

Write-Host "Release complete."
