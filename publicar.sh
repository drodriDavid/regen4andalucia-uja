#!/bin/sh
# Recifra la web y la publica en GitHub Pages.
#
#   ./publicar.sh                 -> mantiene la contrasena actual
#   ./publicar.sh "MI-FRASE"      -> ademas cambia la contrasena a "MI-FRASE"
#
# Funciona desde cualquier carpeta: se situa solo en la del repositorio.

set -e
cd "$(dirname "$0")"

CLAVE="${1:-REGEN4ANDALUCIA}"

echo "→ Cifrando fuente.html…"
python build.py fuente.html --pass "$CLAVE"

echo "→ Publicando…"
git add -A
if git diff --cached --quiet; then
  echo "  (nada que confirmar)"
else
  git commit -q -m "Actualiza la web"
fi
git push -q origin main

echo
echo "Publicado en https://drodridavid.github.io/regen4andalucia-uja/"
echo "Contrasena: $CLAVE"
echo "(GitHub Pages tarda alrededor de un minuto en servir la version nueva.)"
