"""Un unico formato de error para todo el servicio: codigo, mensaje y, si aplica, campos.

- 422 entrada_invalida: no repite el valor recibido (puede traer un RUT o un nombre).
- 404 / 405: errores que lanzan las rutas, con su codigo estable.
- 503 modelo_no_disponible: Gemini no respondio tras los reintentos (riesgo de la matriz:
  caida o cuota de la API); se indica el ingreso manual de contingencia.
- 500 error_interno: mensaje generico hacia fuera; hacia dentro, un log con metodo, ruta y
  tipo de excepcion, nunca su mensaje.
"""
import json

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from servicio.logica import logger

CODIGOS = {404: "no_encontrado", 405: "metodo_no_permitido"}


def error(estado, codigo, mensaje, **extra):
    contenido = {"codigo": codigo, "mensaje": mensaje, **extra}
    return JSONResponse(status_code=estado, content=contenido)


async def entrada_invalida(request, exc):
    campos = []
    for e in exc.errors():
        partes = [p for p in e["loc"][1:] if isinstance(p, str)]
        campos.append(
            {
                "campo": ".".join(partes) or "cuerpo",
                "problema": e["msg"],
            }
        )
    return error(
        422,
        "entrada_invalida",
        "La peticion no cumple el formato esperado.",
        campos=campos,
    )


async def error_http(request, exc):
    codigo = CODIGOS.get(exc.status_code, f"http_{exc.status_code}")
    return error(exc.status_code, codigo, str(exc.detail))


async def modelo_no_disponible(request, exc):
    logger.warning(json.dumps({"evento": "modelo_no_disponible",
                               "metodo": request.method, "ruta": request.url.path}))
    return error(
        503,
        "modelo_no_disponible",
        "El modelo no responde en este momento. Usa el ingreso manual de "
        "contingencia y reintenta mas tarde.",
    )


async def error_interno(request, exc):
    logger.error(json.dumps({"evento": "error_interno", "metodo": request.method,
                             "ruta": request.url.path, "tipo": type(exc).__name__}))
    return error(500, "error_interno", "Ocurrio un error inesperado.")


def registrar(app):
    app.add_exception_handler(RequestValidationError, entrada_invalida)
    app.add_exception_handler(StarletteHTTPException, error_http)
    app.add_exception_handler(TimeoutError, modelo_no_disponible)
    app.add_exception_handler(Exception, error_interno)
