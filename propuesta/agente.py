"""Agente de soporte: arma el modelo, el prompt, la
memoria y el ejecutor con TODAS las herramientas.

Ejecutar desde la raíz del proyecto:
    python propuesta/agente.py
"""
from dotenv import load_dotenv
from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
)
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

from herramientas import HERRAMIENTAS_BAJO_RIESGO
from supervision import (
    HERRAMIENTAS_ALTO_RIESGO,
    registro_aprobaciones,
)
from save_traza import registrar_traza

load_dotenv()

HERRAMIENTAS = (
    HERRAMIENTAS_BAJO_RIESGO + HERRAMIENTAS_ALTO_RIESGO
)

PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un asistente de soporte de envíos. Usa "
        "las herramientas disponibles cuando las "
        "necesites.",
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad"),
])

historiales = {}


def obtener_historial(session_id: str):
    if session_id not in historiales:
        historiales[session_id] = InMemoryChatMessageHistory()
    return historiales[session_id]


def construir_agente():
    """Devuelve el agente listo para invocar, con
    memoria por session_id."""
    modelo = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite"
    )
    agente = create_tool_calling_agent(
        modelo, HERRAMIENTAS, PROMPT
    )
    ejecutor = AgentExecutor(
        agent=agente,
        tools=HERRAMIENTAS,
        return_intermediate_steps=True,
    )
    return RunnableWithMessageHistory(
        ejecutor,
        obtener_historial,
        input_messages_key="entrada",
        history_messages_key="chat_history",
    )


def preguntar(agente, session_id: str, entrada: str) -> str:
    """Invoca al agente, guarda la traza y devuelve la
    respuesta final."""
    resultado = agente.invoke(
        {"entrada": entrada},
        {"configurable": {"session_id": session_id}},
    )
    registrar_traza(
        session_id=session_id,
        entrada=entrada,
        resultado=resultado,
    )
    return resultado["output"]


if __name__ == "__main__":
    agente = construir_agente()

    print(preguntar(
        agente, "cliente_456",
        "¿Cuál es el estado del envío AR12345, "
        "con su historial?",
    ))
    print(preguntar(
        agente, "cliente_789",
        "Reembolsa $1500 del pedido PED789, "
        "llegó dañado.",
    ))
    print("registro:", registro_aprobaciones)
