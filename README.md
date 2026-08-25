# Cuaderno REGEN4ANDALUCIA · UJA

Cuaderno de trabajo interactivo para el seguimiento del proyecto REGEN4ANDALUCIA
(Living Lab andaluz de Agricultura de Conservación y Regenerativa, FEDER
Andalucía 21-27) desde la Universidad de Jaén.

Ocho vistas: panel de situación, tareas, notas, bitácora, documentos del Drive
empotrados, cronograma de 36 meses con hitos, objetivos generales del proyecto y
el encargo concreto de la UJA (actividades, indicadores, presupuesto, fincas,
infraestructura de AEROLAB, equipo y puntos críticos).

Tareas, notas, bitácora, estado de los hitos y enlaces propios se editan desde la
propia página y se guardan en el `localStorage` del navegador. Viven solo en ese
navegador: usa el botón **Copia** para descargar una copia de seguridad en JSON y
**Restaurar** para recuperarla en otro equipo.

**El contenido está cifrado.** Este repositorio es público porque GitHub Pages lo
exige, así que `index.html` no contiene el documento en claro: contiene el
documento cifrado con **AES-256-GCM**, con la clave derivada de una frase de paso
mediante **PBKDF2-HMAC-SHA256** (400.000 iteraciones). El descifrado ocurre
entero en el navegador de quien visita la página; la contraseña no viaja a ningún
servidor ni se almacena.

Sin la contraseña, lo que hay aquí es ruido.

## Identidad

La paleta y el logo salen de la imagen corporativa del proyecto: azul marino
`#22386B`, azules `#1F5FA8` / `#2E6DB4` / `#3E86C6`, verdes `#5E9B3E` / `#74B04B`
/ `#A9CE77` y amarillo `#F5CE4E`. El logotipo va reconstruido como SVG en línea
(mosaico y sol) porque en el Drive solo existe incrustado en el tríptico; si
aparece el original vectorial, sustituye el bloque `MARCA` de `puerta.html` y de
`fuente.html`. Todos los pares de color verificados sobre WCAG AA en tema claro
y oscuro.

## Publicar cambios

Edita `fuente.html` (el documento en claro, ignorado por git) y lanza el script
que corresponda a tu consola. Cifra, confirma y sube en un solo paso.

**PowerShell** (la consola por defecto de Windows):

    cd C:/GEU/regen4andalucia-uja
    .\publicar.ps1

**Git Bash / WSL:**

    cd C:/GEU/regen4andalucia-uja && ./publicar.sh

Para cambiar además la contraseña, pásala como argumento:

    .\publicar.ps1 "MI-FRASE-NUEVA"
    ./publicar.sh  "MI-FRASE-NUEVA"

Sin argumento se mantiene la contraseña actual.

Notas de consola: en **Windows PowerShell 5.1** el operador `&&` no existe (llegó
en PowerShell 7); encadena con `;` o lanza los comandos en líneas separadas.
Y usa barras normales (`C:/GEU/...`): en bash la barra invertida es un carácter
de escape y rompe la ruta.

Cifrar a mano, sin publicar:

    python build.py fuente.html --pass "MI-FRASE"

Requiere Python con el paquete `cryptography`.

## Origen de los datos

Memoria del proyecto, cronograma, presupuestos, reformulación de indicadores
(julio de 2026), actas de las reuniones del 27 de abril y el 22 de mayo de 2026 y
seguimiento de tareas del Drive del consorcio. Estado documentado a 25 de agosto
de 2026.
