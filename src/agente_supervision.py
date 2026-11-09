import queue
import sys
import threading
from datetime import datetime
from langchain_core.tools import tool
import json
from datetime import datetime, timezone
from save_traza import registrar_traza


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
            "'python src/agente_supervision.py'.",
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
        argumentos={"numero_pedido": numero_pedido, "monto": monto},
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

   
if __name__ == "__main__":
    from dotenv import load_dotenv
    from langchain_core.prompts import (
        ChatPromptTemplate,
        MessagesPlaceholder,
    )
    from langchain_google_genai import (
        ChatGoogleGenerativeAI,
    )
    from langchain_classic.agents import (
        AgentExecutor,
        create_tool_calling_agent,
    )

    load_dotenv()
    modelo = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite"
    )
    herramientas = [generar_reembolso]

    prompt_agente = ChatPromptTemplate.from_messages([
        (
            "system",
            "Eres un asistente de soporte. Usa las "
            "herramientas disponibles cuando las "
            "necesites.",
        ),
        ("human", "{entrada}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agente = create_tool_calling_agent(
        modelo, herramientas, prompt_agente
    )
    ejecutor_agente = AgentExecutor(
        agent=agente,
        tools=herramientas, 
        return_intermediate_steps=True,
    )

    pregunta = (
        "Reembolsa $1500 del pedido PED789, "
        "llegó dañado."
    )
    resultado = ejecutor_agente.invoke(
        {"entrada": pregunta}
    )
    registrar_traza(
        session_id="cliente_789",
        entrada=pregunta,
        resultado=resultado,
    )
    print(resultado["output"])
    print("registro:", registro_aprobaciones)


