# Recifra la web y la publica en GitHub Pages.
#
#   .\publicar.ps1                    -> mantiene la contrasena actual
#   .\publicar.ps1 "MI-FRASE-NUEVA"   -> ademas cambia la contrasena
#
# Compatible con Windows PowerShell 5.1. Se situa solo en la carpeta del
# repositorio, asi que da igual desde donde lo lances.

param([string]$Clave = "REGEN4ANDALUCIA")

$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $raiz

Write-Host ""
Write-Host "-> Cifrando fuente.html..." -ForegroundColor DarkGray
python build.py fuente.html --pass $Clave
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: no se pudo cifrar. Revisa que Python y 'cryptography' esten instalados." -ForegroundColor Red
    exit 1
}

Write-Host "-> Publicando en GitHub..." -ForegroundColor DarkGray
git add -A
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: fallo 'git add'." -ForegroundColor Red; exit 1 }

git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Actualiza la web"
    if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: fallo 'git commit'." -ForegroundColor Red; exit 1 }
} else {
    Write-Host "   (no habia cambios que confirmar)" -ForegroundColor DarkGray
}

git push origin main 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: fallo 'git push'. Comprueba tu conexion y que 'gh auth status' sigue activo." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Publicado en https://drodridavid.github.io/regen4andalucia-uja/" -ForegroundColor Green
Write-Host "Contrasena: $Clave"
Write-Host ""
Write-Host "GitHub Pages tarda alrededor de un minuto en servir la version nueva." -ForegroundColor DarkGray
Write-Host "Cuando entres, recarga con Ctrl+F5 para saltarte la cache del navegador." -ForegroundColor DarkGray
