# Compromisos de la UJA en REGEN4ANDALUCIA

Web interactiva con el inventario de compromisos de la Universidad de Jaén en el
proyecto REGEN4ANDALUCIA (Living Lab andaluz de Agricultura de Conservación y
Regenerativa, FEDER Andalucía 21-27): actividades, hitos, indicadores,
presupuesto, fincas, infraestructura, equipo y puntos críticos.

**El contenido está cifrado.** Este repositorio es público porque GitHub Pages lo
exige, así que `index.html` no contiene el documento en claro: contiene el
documento cifrado con **AES-256-GCM**, con la clave derivada de una frase de paso
mediante **PBKDF2-HMAC-SHA256** (400.000 iteraciones). El descifrado ocurre
entero en el navegador de quien visita la página; la contraseña no viaja a ningún
servidor ni se almacena.

Sin la contraseña, lo que hay aquí es ruido.

## Regenerar la página

Hace falta el documento en claro (`fuente.html`, ignorado por git) y Python con
`cryptography`:

```
python build.py fuente.html                 # genera contraseña nueva
python build.py fuente.html --pass "MI-FRASE-DE-PASO"
```

El script escribe `index.html`. Cambiar la contraseña implica volver a ejecutarlo
y publicar el `index.html` resultante.

## Origen de los datos

Memoria del proyecto, cronograma, presupuestos, reformulación de indicadores
(julio de 2026), actas de las reuniones del 27 de abril y el 22 de mayo de 2026 y
seguimiento de tareas del Drive del consorcio. Estado documentado a 25 de agosto
de 2026.
