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
    return plantilla().replace("__SALT__", salt_b64) \
                    .replace("__IV__", iv_b64) \
                    .replace("__ITER__", str(ITERATIONS)) \
                    .replace("__BLOB__", blob)


def plantilla():
    """La portada con el formulario de contrasena vive en puerta.html."""
    return io.open("puerta.html", encoding="utf-8").read()


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
