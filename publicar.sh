#!/bin/sh
# Recifra el cuaderno y lo publica en GitHub Pages.
#
#   ./publicar.sh                 -> mantiene la clave actual
#   ./publicar.sh "CLAVE-NUEVA"   -> ademas cambia la clave
#
# La clave se guarda en clave.txt, que git ignora: el repositorio es publico
# y ahi dentro no puede haber nada que abra el cuaderno.

set -e
cd "$(dirname "$0")"

CLAVE="$1"
if [ -z "$CLAVE" ]; then
  if [ ! -f clave.txt ]; then
    echo "ERROR: falta clave.txt y no has pasado ninguna clave." >&2
    exit 1
  fi
  CLAVE=$(tr -d ' \t\r\n' < clave.txt)
fi

echo "-> Cifrando fuente.html..."
python build.py fuente.html --pass "$CLAVE"
printf '%s' "$CLAVE" > clave.txt

echo "-> Publicando..."
git add -A
if git diff --cached --quiet; then
  echo "   (nada que confirmar)"
else
  git commit -q -m "Actualiza el cuaderno"
fi
git push -q origin main

echo
echo "Publicado en https://drodridavid.github.io/regen4andalucia-uja/"
echo "Si has cambiado la clave, borra clave-cuaderno.txt de la carpeta de Drive"
echo "'Cuaderno REGEN4ANDALUCIA (UJA)' y vuelve a entrar para dejar la nueva."
