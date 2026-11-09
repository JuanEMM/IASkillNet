"""Herramientas de riesgo ALTO y su supervisión humana.

Todo lo que mueve dinero o no se puede deshacer vive
aquí, junto con el mecanismo de aprobación y su registro.
"""
import queue
import sys
import threading
from datetime import datetime
from langchain_core.tools import tool

registro_aprobaciones = []


def esperar_aprobacion(
    mensaje: str,
    tiempo_limite_segundos: int = 300
) -> bool:
    print(mensaje, flush=True)
    cola = queue.Queue()
    # select.select no funciona con stdin en Windows,
    # así que se lee en un hilo y se espera con timeout.
    threading.Thread(
        target=lambda: cola.put(sys.stdin.readline()),
        daemon=True,
    ).start()
    try:
        respuesta = cola.get(timeout=tiempo_limite_segundos)
    except queue.Empty:
        return False
    if respuesta == "":
        # readline() devuelve "" solo cuando stdin está
        # cerrado (EOF): no hay terminal interactiva.
        print(
            "stdin no está disponible: no puedo pedir "
            "aprobación, se rechaza por seguridad. "
            "Ejecuta desde una terminal con "
            "'python propuesta/agente.py'.",
            flush=True,
        )
        return False
    return respuesta.strip().lower() == "s"


def registrar_aprobacion(
    herramienta: str,
    argumentos: dict,
    aprobado: bool,
) -> None:
    registro_aprobaciones.append({
        "herramienta": herramienta,
        "argumentos": argumentos,
        "aprobado": aprobado,
        "momento": datetime.now().isoformat(),
    })


@tool
def generar_reembolso(numero_pedido: str, monto: float) -> str:
    """Genera un reembolso para un pedido. Acción
    irreversible: requiere aprobación humana antes
    de ejecutarse."""
    mensaje = (
        f"El agente quiere reembolsar ${monto} "
        f"para el pedido {numero_pedido}. "
        f"¿Aprobar? (s/n): "
    )
    aprobado = esperar_aprobacion(mensaje)
    registrar_aprobacion(
        herramienta="generar_reembolso",
        argumentos={
            "numero_pedido": numero_pedido,
            "monto": monto,
        },
        aprobado=aprobado,
    )

    if not aprobado:
        return (
            "Reembolso no aprobado por el "
            "supervisor humano."
        )

    return (
        f"Reembolso de ${monto} generado para "
        f"el pedido {numero_pedido}."
    )


HERRAMIENTAS_ALTO_RIESGO = [generar_reembolso]
