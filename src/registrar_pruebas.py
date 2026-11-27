"""Comprueba la cobertura de la tabla de casos, la ejecuta por HTTP real y escribe el registro.

Uso, desde la raiz del repositorio y con el servicio arrancado en otra terminal
(uvicorn servicio.main:app --app-dir src --reload):
    python src/registrar_pruebas.py
    python src/registrar_pruebas.py http://127.0.0.1:8001
Escribe docs/registro_pruebas.md. Termina con codigo 1 si la tabla no cumple la cobertura
minima, si el servicio no responde o si algun caso falla.
"""
import json
import os
import sys
from datetime import date

import httpx2

from casos import CASOS, ejecutar_caso

RUTA = "docs/registro_pruebas.md"
ESTADOS_OBLIGATORIOS = (404, 405, 422)
COLUMNAS = (
    "Caso", "Descripción", "Petición",
    "Esperado", "Obtenido", "Resultado",
)
# Las consultas reales tardan hasta 45,7 s en el Gate 2 y RNF-02 admite hasta 60 s
TIMEOUT_S = 60


def verificar_cobertura(casos):
    errores = []
    validos = [c for c in casos if c["id"].startswith("V-")]
    invalidos = [c for c in casos if c["id"].startswith("I-")]
    if len(validos) < 3:
        errores.append(f"hay {len(validos)} casos validos y se piden 3")
    if len(invalidos) < 5:
        errores.append(
            f"hay {len(invalidos)} casos invalidos y se piden 5"
        )
    esperados = {c["estado"] for c in invalidos}
    for estado in ESTADOS_OBLIGATORIOS:
        if estado not in esperados:
            errores.append(
                f"ningun caso invalido espera el estado {estado}"
            )
    return errores


def describir(caso):
    cuerpo = caso.get("contenido")
    if cuerpo is None and "json" in caso:
        cuerpo = json.dumps(caso["json"], ensure_ascii=False)
    texto = f"{caso['metodo']} {caso['ruta']}"
    if cuerpo:
        corto = cuerpo if len(cuerpo) <= 40 else cuerpo[:40] + "..."
        texto += f" {corto}"
    return texto.replace("|", "/")


def registrar(base_url):
    filas = []
    with httpx2.Client(base_url=base_url, timeout=TIMEOUT_S) as cliente:
        for caso in CASOS:
            try:
                ok, estado, _ = ejecutar_caso(cliente, caso)
            except httpx2.TimeoutException:
                ok, estado = False, f"sin respuesta en {TIMEOUT_S} s"
            filas.append((caso, ok, estado))
    cumplidos = sum(1 for _, ok, _ in filas if ok)
    lineas = [
        "# Registro de pruebas de la API",
        f"Fecha: {date.today()}",
        f"Servicio probado: {base_url} (cliente: httpx2)",
        f"Resultado: {cumplidos} de {len(filas)} casos cumplidos",
        "",
        "| " + " | ".join(COLUMNAS) + " |",
        "|" + "---|" * len(COLUMNAS),
    ]
    for caso, ok, estado in filas:
        veredicto = "PASA" if ok else "FALLA"
        lineas.append(
            f"| {caso['id']} | {caso['descripcion']} "
            f"| {describir(caso)} | {caso['estado']} "
            f"| {estado} | {veredicto} |"
        )
    os.makedirs("docs", exist_ok=True)
    with open(RUTA, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
    return cumplidos, len(filas)


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    errores = verificar_cobertura(CASOS)
    for error in errores:
        print("ERROR:", error)
    if errores:
        sys.exit(1)
    try:
        cumplidos, total = registrar(base)
    except httpx2.ConnectError:
        sys.exit(f"No se pudo conectar a {base}. Arranca el servicio.")
    print(f"Registro escrito en {RUTA}: {cumplidos} de {total} casos")
    sys.exit(0 if cumplidos == total else 1)
