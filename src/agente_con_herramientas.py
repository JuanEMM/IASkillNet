from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

 
load_dotenv()
modelo = ChatGoogleGenerativeAI(model="gemini-3.8-flash")
from langchain_core.tools import tool

from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
@tool
def consultar_estado_envio(numero_seguimiento: str) -> str:
    """Consulta el estado actual de un envío a
    partir de su número de seguimiento. Usar
    cuando el usuario pregunta dónde está su
    pedido."""
    estados = {
        "AR12345": (
            "en tránsito, llega en 2 días"
        ),
        "AR67890": "entregado"
    }

    try:
        return estados[numero_seguimiento]
    except KeyError:
        return (
            f"No se encontró un envío con el "
            f"número {numero_seguimiento}."
        )
@tool
def calcular_costo_envio(
    peso_kg: float,
    distancia_km: float
) -> str:
    """Calcula el costo estimado de un envío
    según su peso y la distancia a recorrer.
    Usar cuando el usuario pregunta cuánto va a
    costar enviar algo."""
    costo = 500 + (peso_kg * 120) + (distancia_km * 3)

    return f"El costo estimado es de ${costo:.2f}."


    
herramientas = [consultar_estado_envio, calcular_costo_envio]

prompt_agente = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un asistente que responde preguntas "
        "usando las herramientas disponibles cuando "
        "las necesites.",
    ),
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agente = create_tool_calling_agent(
    modelo, herramientas, prompt_agente
)

ejecutor_agente = AgentExecutor(
    agent=agente, tools=herramientas, verbose=True,  return_intermediate_steps=True,
)
 
resultado = ejecutor_agente.invoke({
    "entrada": (
        "¿Dónde está mi pedido AR12345?"
    )
})

herramienta_usada = (
    resultado["intermediate_steps"][0][0].tool
)

assert herramienta_usada == "consultar_estado_envio"
print(resultado["output"])

def test_agente_no_usa_herramienta_para_pregunta_general():

    resultado = ejecutor_agente.invoke({
        "entrada": (
            "¿Cómo puedo contactar a soporte?"
        )
    })

    assert resultado["intermediate_steps"] == []