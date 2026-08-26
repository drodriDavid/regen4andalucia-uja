# Recifra el cuaderno y lo publica en GitHub Pages.
#
#   .\publicar.ps1                    -> mantiene la clave actual
#   .\publicar.ps1 "CLAVE-NUEVA"      -> ademas cambia la clave
#
# La clave se guarda en clave.txt, que git ignora: el repositorio es publico
# y ahi dentro no puede haber nada que abra el cuaderno. Quien entra en la
# web no la escribe: la portada la lee de la carpeta de Drive.
#
# Compatible con Windows PowerShell 5.1. Se situa solo en la carpeta del
# repositorio, asi que da igual desde donde lo lances.

param([string]$Clave = "")

$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $raiz

# Nada en claro vive aqui: las piezas y la clave estan en el repositorio
# privado de fuentes, al lado de este.
$fuentes = Join-Path (Split-Path -Parent $raiz) ("fuentes\" + (Split-Path -Leaf $raiz))
if (-not (Test-Path $fuentes)) {
    Write-Host "ERROR: no encuentro las fuentes en $fuentes" -ForegroundColor Red
    Write-Host "       Clona el repositorio privado de fuentes en la carpeta 'fuentes'," -ForegroundColor DarkGray
    Write-Host "       al lado de este repositorio." -ForegroundColor DarkGray
    exit 1
}

if ($Clave -eq "") {
    if (-not (Test-Path (Join-Path $fuentes "clave.txt"))) {
        Write-Host "ERROR: falta clave.txt y no has pasado ninguna clave." -ForegroundColor Red
        Write-Host "       Escribe la clave del cuaderno en clave.txt, o lanza:" -ForegroundColor DarkGray
        Write-Host '       .\publicar.ps1 "TU-CLAVE"' -ForegroundColor DarkGray
        exit 1
    }
    $Clave = (Get-Content (Join-Path $fuentes "clave.txt") -Raw).Trim()
}

Write-Host ""
Write-Host "-> Cifrando fuente.html..." -ForegroundColor DarkGray
python build.py (Join-Path $fuentes "fuente.html") --pass $Clave
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: no se pudo cifrar. Revisa que Python y 'cryptography' esten instalados." -ForegroundColor Red
    exit 1
}
Set-Content -Path (Join-Path $fuentes "clave.txt") -Value $Clave -NoNewline -Encoding UTF8

Write-Host "-> Publicando en GitHub..." -ForegroundColor DarkGray
git add -A
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: fallo 'git add'." -ForegroundColor Red; exit 1 }

git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Actualiza el cuaderno"
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
Write-Host ""
Write-Host "Si has cambiado la clave, borra clave-cuaderno.txt de la carpeta de Drive" -ForegroundColor Yellow
Write-Host "'Cuaderno REGEN4ANDALUCIA (UJA)' y vuelve a entrar para dejar la nueva." -ForegroundColor Yellow
Write-Host ""
Write-Host "GitHub Pages tarda alrededor de un minuto en servir la version nueva." -ForegroundColor DarkGray
Write-Host "Cuando entres, recarga con Ctrl+F5 para saltarte la cache del navegador." -ForegroundColor DarkGray
