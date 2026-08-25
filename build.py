#!/usr/bin/env python3
"""
Cifra la web de compromisos de la UJA y genera el index.html que la sirve
tras pedir la contrasena.

El contenido se cifra con AES-256-GCM y la clave se deriva de la frase de
paso con PBKDF2-HMAC-SHA256. Lo que se publica en GitHub Pages es texto
cifrado: sin la contrasena no hay nada legible en el repositorio.

Uso:
    python build.py <fuente.html> [--pass FRASE]

Sin --pass genera una frase de paso aleatoria de 80 bits y la imprime.
"""

import argparse
import base64
import hashlib
import io
import os
import secrets
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITERATIONS = 400_000
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # sin I, O, 0, 1
PASS_CHARS = 16  # 16 * 5 bits = 80 bits de entropia

DOC_HEAD = (
    '<!doctype html>\n<html lang="es">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    '<meta name="robots" content="noindex,nofollow">\n'
)


def genera_frase():
    bruto = "".join(secrets.choice(ALPHABET) for _ in range(PASS_CHARS))
    return "-".join(bruto[i:i + 4] for i in range(0, PASS_CHARS, 4))


def documento_completo(fragmento):
    """Envuelve el fragmento del artifact en un documento HTML autonomo."""
    return DOC_HEAD + fragmento + "\n</html>\n"


def cifra(texto, frase):
    salt = os.urandom(16)
    iv = os.urandom(12)
    clave = hashlib.pbkdf2_hmac("sha256", frase.encode("utf-8"), salt, ITERATIONS, 32)
    ct = AESGCM(clave).encrypt(iv, texto.encode("utf-8"), None)
    b64 = base64.b64encode
    return b64(salt).decode(), b64(iv).decode(), b64(ct).decode()


def portada(salt_b64, iv_b64, ct_b64):
    # El blob va troceado en lineas para que el archivo siga siendo legible en git.
    trozos = [ct_b64[i:i + 120] for i in range(0, len(ct_b64), 120)]
    blob = "\n".join('"' + t + '",' for t in trozos)
    return PLANTILLA.replace("__SALT__", salt_b64) \
                    .replace("__IV__", iv_b64) \
                    .replace("__ITER__", str(ITERATIONS)) \
                    .replace("__BLOB__", blob)


PLANTILLA = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Compromisos UJA en REGEN4ANDALUCIA</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
:root{
  --bg:#F1F2ED; --surface:#FBFBF8; --surface-2:#E6E9DF; --line:#D4D8CA;
  --ink:#191E16; --ink-2:#485043; --ink-3:#6D7667;
  --field:#54721E; --risk:#98381F; --on-accent:#FBFBF8;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#111409; --surface:#191D13; --surface-2:#232819; --line:#333A28;
    --ink:#ECEFE3; --ink-2:#B2B9A5; --ink-3:#858D78;
    --field:#A3C954; --risk:#E37A5C; --on-accent:#111409;
  }
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"Archivo","Helvetica Neue",Arial,sans-serif; font-size:16px; line-height:1.55;
  display:grid; place-items:center; padding:24px; -webkit-font-smoothing:antialiased;
}
.gate{width:100%; max-width:420px}
.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-3);
}
h1{
  font-family:"Fraunces",Georgia,serif; font-weight:600; font-size:30px; line-height:1.1;
  letter-spacing:-.02em; margin:12px 0 0; text-wrap:balance;
}
h1 em{font-style:normal; color:var(--field)}
.sub{color:var(--ink-2); font-size:14.5px; margin:12px 0 0}
form{
  margin-top:26px; background:var(--surface); border:1px solid var(--line); border-radius:4px;
  padding:20px; display:flex; flex-direction:column; gap:12px;
}
label{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10.5px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3);
}
input{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:15px; letter-spacing:.06em;
  padding:11px 13px; border:1px solid var(--line); border-radius:3px;
  background:var(--bg); color:var(--ink); width:100%;
}
input:focus{outline:2px solid var(--field); outline-offset:1px; border-color:var(--field)}
button{
  font:inherit; font-size:14.5px; font-weight:600; padding:11px 16px; border:0; border-radius:3px;
  background:var(--field); color:var(--on-accent); cursor:pointer;
}
button:hover{filter:brightness(1.08)}
button:disabled{opacity:.55; cursor:progress}
button:focus-visible{outline:2px solid var(--ink); outline-offset:2px}
.msg{font-size:13.5px; min-height:20px; color:var(--risk)}
.msg.work{color:var(--ink-3)}
.foot{margin-top:20px; font-size:12.5px; color:var(--ink-3); line-height:1.5}
</style>
</head>
<body>

<main class="gate">
  <p class="eyebrow">REGEN4ANDALUCIA &middot; FEDER Andaluc&iacute;a 21-27</p>
  <h1>Compromisos de la <em>UJA</em></h1>
  <p class="sub">
    Documento interno del proyecto. El contenido de esta p&aacute;gina est&aacute; cifrado:
    introduce la contrase&ntilde;a para descifrarlo en tu navegador.
  </p>

  <form id="f" autocomplete="off">
    <label for="p">Contrase&ntilde;a</label>
    <input id="p" type="password" inputmode="text" autocapitalize="characters"
           spellcheck="false" placeholder="XXXX-XXXX-XXXX-XXXX" autofocus>
    <button id="b" type="submit">Abrir el documento</button>
    <p class="msg" id="m" role="status" aria-live="polite"></p>
  </form>

  <p class="foot">
    El descifrado ocurre en tu navegador (AES-256-GCM, clave derivada con PBKDF2).
    La contrase&ntilde;a no se env&iacute;a a ning&uacute;n servidor ni se guarda en ning&uacute;n sitio.
  </p>
</main>

<script>
(function(){
  "use strict";

  var SALT = "__SALT__";
  var IV   = "__IV__";
  var ITER = __ITER__;
  var CT   = [
__BLOB__
  ].join("");

  function bytes(b64){
    var bin = atob(b64), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  var form = document.getElementById("f");
  var input = document.getElementById("p");
  var boton = document.getElementById("b");
  var msg = document.getElementById("m");

  if (!window.crypto || !window.crypto.subtle){
    msg.textContent = "Este navegador no permite descifrar la página. Prueba con Chrome, Firefox, Edge o Safari actualizados, y sobre https.";
    boton.disabled = true;
    return;
  }

  function estado(texto, trabajando){
    msg.textContent = texto;
    msg.className = trabajando ? "msg work" : "msg";
  }

  form.addEventListener("submit", function(ev){
    ev.preventDefault();
    var frase = input.value.trim().toUpperCase();
    if (!frase){ estado("Escribe la contraseña.", false); return; }

    boton.disabled = true;
    estado("Descifrando…", true);

    // Un respiro para que el navegador pinte el estado antes del PBKDF2.
    setTimeout(function(){
      crypto.subtle.importKey("raw", new TextEncoder().encode(frase), "PBKDF2", false, ["deriveKey"])
        .then(function(km){
          return crypto.subtle.deriveKey(
            {name:"PBKDF2", salt:bytes(SALT), iterations:ITER, hash:"SHA-256"},
            km, {name:"AES-GCM", length:256}, false, ["decrypt"]);
        })
        .then(function(key){
          return crypto.subtle.decrypt({name:"AES-GCM", iv:bytes(IV)}, key, bytes(CT));
        })
        .then(function(plano){
          var html = new TextDecoder().decode(plano);
          document.open();
          document.write(html);
          document.close();
        })
        .catch(function(){
          boton.disabled = false;
          estado("Contraseña incorrecta.", false);
          input.select();
        });
    }, 30);
  });
})();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fuente")
    ap.add_argument("--pass", dest="frase", default=None)
    ap.add_argument("--salida", default="index.html")
    args = ap.parse_args()

    fragmento = io.open(args.fuente, encoding="utf-8").read()
    doc = documento_completo(fragmento)

    frase = args.frase or genera_frase()
    salt_b64, iv_b64, ct_b64 = cifra(doc, frase)

    io.open(args.salida, "w", encoding="utf-8").write(portada(salt_b64, iv_b64, ct_b64))

    print("contrasena: " + frase)
    print("iteraciones: %d" % ITERATIONS)
    print("documento en claro: %d bytes" % len(doc.encode("utf-8")))
    print("salida: %s (%d bytes)" % (args.salida, os.path.getsize(args.salida)))


if __name__ == "__main__":
    sys.exit(main())
