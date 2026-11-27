"""La capa HTTP del servicio de porteria. Sin logica de negocio: llama a logica.py.

Arranque, desde la raiz del repositorio (ahi estan .env e indice_gate2/):
    uvicorn servicio.main:app --app-dir src --reload
"""
from fastapi import FastAPI

from servicio import logica
from servicio.esquemas import Consulta, Guia, RespuestaConsulta, RespuestaExtraccion

app = FastAPI(
    title="Servicio de porteria",
    version="0.1.0",
    description="Extrae los datos de las guias de transporte y responde consultas sobre los "
                "ingresos de camiones y los procedimientos de porteria, con la fuente de cada dato.",
)


@app.get("/salud", tags=["sistema"], summary="Comprobar el servicio")
def salud():
    return {"estado": "ok"}


@app.post(
    "/extracciones",
    response_model=RespuestaExtraccion,
    tags=["extracciones"],
    summary="Extraer los datos de una guia",
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
)
def consultar(consulta: Consulta):
    """Devuelve los datos encontrados en los procedimientos y en los registros de ingreso.

    Cada item trae su fuente. Si los documentos no cubren la pregunta, items va vacia.
    """
    return RespuestaConsulta(**logica.responder(consulta.pregunta))
