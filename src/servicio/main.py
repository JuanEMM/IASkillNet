"""La capa HTTP del servicio de porteria. Sin logica de negocio: llama a logica.py.

Arranque, desde la raiz del repositorio (ahi estan .env e indice_gate2/):
    uvicorn servicio.main:app --app-dir src --reload
"""
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

from servicio import logica
from servicio.errores import registrar
from servicio.esquemas import (
    Consulta,
    ErrorRespuesta,
    EstadoIngreso,
    Guia,
    RespuestaConsulta,
    RespuestaExtraccion,
)

app = FastAPI(
    title="Servicio de porteria",
    version="0.2.0",
    description="Extrae los datos de las guias de transporte y responde consultas sobre los "
                "ingresos de camiones y los procedimientos de porteria, con la fuente de cada dato.",
)
registrar(app)

ENTRADA_INVALIDA = {422: {"model": ErrorRespuesta, "description": "Entrada invalida."}}
NO_ENCONTRADO = {404: {"model": ErrorRespuesta, "description": "La patente no tiene ingreso hoy."}}
MODELO_NO_DISPONIBLE = {
    503: {
        "model": ErrorRespuesta,
        "description": "Gemini no responde tras los reintentos: usar el ingreso manual de contingencia.",
    }
}
PATENTE = r"^(?:[A-Za-z]{4}\d{2}|[A-Za-z]{2}\d{4})$"


@app.get("/salud", tags=["sistema"], summary="Comprobar el servicio")
def salud():
    return {"estado": "ok"}


@app.post(
    "/extracciones",
    response_model=RespuestaExtraccion,
    tags=["extracciones"],
    summary="Extraer los datos de una guia",
    responses={**ENTRADA_INVALIDA, **MODELO_NO_DISPONIBLE},
)
def extraer(guia: Guia):
    """Extrae los datos de la guia y marca los que el guardia debe confirmar.

    La patente y el RUT se validan por codigo: un dato invalido o con calidad
    menor a 4 trae requiere_confirmacion en true.
    """
    return RespuestaExtraccion(**logica.extraer_guia(guia.texto))


@app.post(
    "/consultas",
    response_model=RespuestaConsulta,
    tags=["consultas"],
    summary="Consultar ingresos y procedimientos",
    responses={**ENTRADA_INVALIDA, **MODELO_NO_DISPONIBLE},
)
def consultar(consulta: Consulta):
    """Devuelve los datos encontrados en los procedimientos y en los registros de ingreso.

    Cada item trae su fuente. Si los documentos no cubren la pregunta, items va vacia.
    """
    return RespuestaConsulta(**logica.responder(consulta.pregunta))


@app.get(
    "/ingresos/{patente}",
    response_model=EstadoIngreso,
    tags=["ingresos"],
    summary="Consultar el ingreso de hoy de un camion",
    responses={**NO_ENCONTRADO, **ENTRADA_INVALIDA},
)
def consultar_ingreso(
    patente: Annotated[
        str,
        Path(
            pattern=PATENTE,
            description="Patente chilena: cuatro letras y dos digitos (BXKL45) o dos letras y cuatro digitos (AB1234).",
            examples=["BXKL45"],
        ),
    ],
):
    """Busca el ingreso de hoy en el registro simulado, sin llamar al modelo."""
    ingreso = logica.ingreso_de_hoy(patente)
    if ingreso is None:
        raise HTTPException(404, f"La patente {patente.upper()} no tiene ingreso registrado hoy.")
    return EstadoIngreso(**ingreso)
