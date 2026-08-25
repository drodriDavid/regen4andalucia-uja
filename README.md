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
