# Cuaderno REGEN4ANDALUCIA · UJA

Cuaderno de trabajo interactivo para el seguimiento del proyecto REGEN4ANDALUCIA
(Living Lab andaluz de Agricultura de Conservación y Regenerativa, FEDER
Andalucía 21-27) desde la Universidad de Jaén.

Nueve vistas: resumen del proyecto, panel de situación, tareas, notas, bitácora,
documentos del Drive empotrados, personas del Living Lab, cronograma de 36 meses
con hitos y presupuesto con registro de gasto.

## Cómo se entra

Se entra **con cuenta de Google**. No hay contraseña que escribir.

El repositorio es público porque GitHub Pages lo exige, así que `index.html` no
contiene el documento en claro: contiene el documento cifrado con **AES-256-GCM**,
con la clave derivada mediante **PBKDF2-HMAC-SHA256** (400.000 iteraciones). Sin
la clave, lo que hay aquí es ruido.

La clave no la teclea nadie: vive en un archivo `clave-cuaderno.txt` dentro de la
carpeta de Drive **Cuaderno REGEN4ANDALUCIA (UJA)**. Al pulsar «Entrar con
Google», la portada pide acceso a Drive, busca esa carpeta, lee la clave y
descifra la página en el propio navegador. Quien no tenga la carpeta compartida
no puede leer nada.

Así que el control de acceso es el de Google: **compartir esa carpeta de Drive es
dar acceso al cuaderno, y dejar de compartirla es quitarlo.** La carpeta es
propia, nunca la del consorcio.

La primera vez que se estrena una clave nueva, la portada pide pegarla una sola
vez y la deja guardada en Drive para que nadie más tenga que hacerlo.

## Sincronización

El cuaderno se conecta solo al entrar. Todo lo que se escribe (tareas, notas,
bitácora, estados de hitos y riesgos, gasto) se guarda en
`cuaderno-regen4andalucia-uja.json`, en esa misma carpeta de Drive, a los pocos
segundos de cada cambio. Al abrir la página y al volver a la pestaña, el cuaderno
comprueba si alguien ha escrito y trae lo nuevo.

El indicador de la barra superior muestra el estado y, si algo falla, permite
volver a conectar a mano.

Los permisos que pide son de Drive completo, porque tiene que poder abrir y
escribir un archivo que quizá creó otra persona del equipo. El ID de cliente
OAuth va incrustado en la página: es público por diseño y no es un secreto.

## Drive en vivo

La pestaña Drive trae un índice incrustado de la carpeta del consorcio (foto del
25 de agosto de 2026) y, con la sesión de Google ya iniciada al entrar, lee la
carpeta real y refleja lo que haya en cada momento.

## Publicar cambios

Edita `fuente.html` (el documento en claro, ignorado por git) y lanza el script
que corresponda a tu consola. Cifra, confirma y sube en un solo paso.

**PowerShell** (la consola por defecto de Windows):

    cd C:/ProyectosUJA/regen4andalucia-uja
    .\publicar.ps1

**Git Bash / WSL:**

    cd C:/ProyectosUJA/regen4andalucia-uja && ./publicar.sh

La clave se lee de `clave.txt`, que git ignora. Para cambiarla, pásala como
argumento:

    .\publicar.ps1 "CLAVE-NUEVA"
    ./publicar.sh  "CLAVE-NUEVA"

Si la cambias, **borra `clave-cuaderno.txt` de la carpeta de Drive** y vuelve a
entrar una vez para dejar la nueva; si no, la portada seguirá intentando abrir
con la vieja y se la pedirá a cada persona.

Antes de cifrar conviene validar el JavaScript: extraer el `<script>` de
`fuente.html` y de `puerta.html` y pasarles `node --check`. En este proyecto han
aparecido varias colisiones de nombres que rompieron la página en silencio.

Notas de consola: en **Windows PowerShell 5.1** el operador `&&` no existe (llegó
en PowerShell 7); encadena con `;` o lanza los comandos en líneas separadas.
Y usa barras normales (`C:/ProyectosUJA/...`): en bash la barra invertida es un carácter
de escape y rompe la ruta.

Cifrar a mano, sin publicar:

    python build.py fuente.html --pass "MI-CLAVE"

Requiere Python con el paquete `cryptography`.

## Identidad

La paleta y el logo salen de la imagen corporativa del proyecto: azul marino
`#22386B`, azules `#1F5FA8` / `#2E6DB4` / `#3E86C6`, verdes `#5E9B3E` / `#74B04B`
/ `#A9CE77` y amarillo `#F5CE4E`. El logotipo original va incrustado como data
URI en `logo.b64`, que `build.py` inyecta en la portada. Todos los pares de color
verificados sobre WCAG AA en tema claro y oscuro.

## Origen de los datos

Memoria del proyecto, cronograma, presupuestos, reformulación de indicadores
(julio de 2026), actas de las reuniones del 27 de abril y el 22 de mayo de 2026 y
seguimiento de tareas del Drive del consorcio. Estado documentado a 25 de agosto
de 2026.
