"""Herramientas de riesgo BAJO: solo leen o calculan.

No modifican nada ni ejecutan acciones externas, por lo
que el agente puede usarlas sin supervisión humana.
"""
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class ArgumentosConsultaEnvio(BaseModel):
    numero_seguimiento: str = Field(
        description="Número de seguimiento del envío."
    )
    incluir_historial: bool = Field(
        default=False,
        description="Si es True, incluye el historial completo."
    )


ESTADOS = {
    "AR12345": {
        "actual": "en tránsito, llega en 2 días",
        "historial": [
            "recibido en depósito",
            "en tránsito",
        ],
    },
}


@tool(
    "consultar_estado_envio_con_historial",
    args_schema=ArgumentosConsultaEnvio
)
def consultar_estado_envio_detallado(
    numero_seguimiento: str,
    incluir_historial: bool = False
) -> str:
    """Consulta el estado de un envío, con la
    opción de incluir su historial completo."""
    envio = ESTADOS.get(numero_seguimiento)
    if envio is None:
        return (
            f"No se encontró un envío con el "
            f"número {numero_seguimiento}."
        )
    if not incluir_historial:
        return envio["actual"]
    historial = ", ".join(envio["historial"])
    return f"{envio['actual']} (historial: {historial})"


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


HERRAMIENTAS_BAJO_RIESGO = [
    consultar_estado_envio_detallado,
    calcular_costo_envio,
]
