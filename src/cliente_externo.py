"""Ejecuta la tabla de casos contra el servicio en ejecucion, por HTTP real (Bloque 36).

Uso, desde la raiz del repositorio y con el servicio arrancado en otra terminal
(uvicorn servicio.main:app --app-dir src --reload):
    python src/cliente_externo.py
    python src/cliente_externo.py http://127.0.0.1:8001
Termina con codigo 0 si todos los casos se cumplen y con 1 si alguno falla.
"""
import sys

import httpx2

from casos import CASOS, ejecutar_caso

# Las consultas reales tardan hasta 45,7 s en el Gate 2 y RNF-02 admite hasta 60 s
TIMEOUT_S = 60


def main(base_url):
    # Comprobacion de salud antes de ejecutar todos los casos
    with httpx2.Client(base_url=base_url, timeout=5) as chk:
        res = chk.get("/salud")
        if res.status_code != 200:
            print(f"El servicio respondio con estado {res.status_code} en /salud.")
            return False
    cumplidos = 0
    with httpx2.Client(base_url=base_url, timeout=TIMEOUT_S) as cliente:
        for caso in CASOS:
            try:
                ok, estado, _ = ejecutar_caso(cliente, caso)
            except httpx2.TimeoutException:
                ok, estado = False, f"sin respuesta en {TIMEOUT_S} s"
            veredicto = "PASA " if ok else "FALLA"
            print(
                f"{veredicto} {caso['id']} {caso['metodo']} "
                f"{caso['ruta']} -> esperado {caso['estado']}, "
                f"obtenido {estado}"
            )
            cumplidos += 1 if ok else 0
    print(f"\n{cumplidos} de {len(CASOS)} casos cumplidos")
    return cumplidos == len(CASOS)


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    try:
        resultado = main(base)
    except httpx2.ConnectError:
        sys.exit(f"No se pudo conectar a {base}. Arranca el servicio.")
    sys.exit(0 if resultado else 1)
