"""Tabla de casos del servicio de porteria (Bloque 36): una peticion y lo que se espera de ella.

V-NN son casos validos e I-NN invalidos. "contiene" es un fragmento estable que senala el
comportamiento (la fuente, la lista vacia, el codigo de error), no la redaccion exacta.
Los casos con "modelo": True llaman a Gemini (V-01, V-02 y V-05); el resto no. Las
descripciones nombran el criterio de aceptacion de la ficha (seccion 4) que cubre cada caso.
"""
from servicio.esquemas import GUIA_EJEMPLO

LARGA = "a" * 600
GUIA_LARGA = "g" * 2001

CASOS = [
    {"id": "V-01", "descripcion": "CA-04/CA-05: consulta por patente con su fuente", "modelo": True,
     "metodo": "POST", "ruta": "/consultas",
     "json": {"pregunta": "cuando ingreso el camion BXKL45"},
     "estado": 200, "contiene": '"fuente":"ingreso-0007"'},
    {"id": "V-02", "descripcion": "CA-06: consulta que los documentos no cubren", "modelo": True,
     "metodo": "POST", "ruta": "/consultas",
     "json": {"pregunta": "cual es el horario del casino de la planta"},
     "estado": 200, "contiene": '"items":[]'},
    {"id": "V-03", "descripcion": "ingreso de hoy de una patente existente",
     "metodo": "GET", "ruta": "/ingresos/BXKL45",
     "estado": 200, "contiene": '"fuente":"ingreso-0007"'},
    {"id": "V-04", "descripcion": "comprobacion de salud",
     "metodo": "GET", "ruta": "/salud",
     "estado": 200, "contiene": "ok"},
    {"id": "V-05", "descripcion": "CA-01: extraccion de una guia valida", "modelo": True,
     "metodo": "POST", "ruta": "/extracciones",
     "json": {"texto": GUIA_EJEMPLO},
     "estado": 200, "contiene": '"requiere_confirmacion"'},
    {"id": "I-01", "descripcion": "falta el campo pregunta",
     "metodo": "POST", "ruta": "/consultas", "json": {},
     "estado": 422, "contiene": "entrada_invalida"},
    {"id": "I-02", "descripcion": "pregunta vacia",
     "metodo": "POST", "ruta": "/consultas", "json": {"pregunta": ""},
     "estado": 422, "contiene": "at least 3 characters"},
    {"id": "I-03", "descripcion": "pregunta solo con espacios",
     "metodo": "POST", "ruta": "/consultas", "json": {"pregunta": "   "},
     "estado": 422, "contiene": "at least 3 characters"},
    {"id": "I-04", "descripcion": "pregunta de 600 caracteres",
     "metodo": "POST", "ruta": "/consultas", "json": {"pregunta": LARGA},
     "estado": 422, "contiene": "at most 500 characters"},
    {"id": "I-05", "descripcion": "pregunta con tipo incorrecto",
     "metodo": "POST", "ruta": "/consultas", "json": {"pregunta": 123},
     "estado": 422, "contiene": "valid string"},
    {"id": "I-06", "descripcion": "cuerpo que no es JSON valido",
     "metodo": "POST", "ruta": "/consultas", "contenido": '{"pregunta": ',
     "estado": 422, "contiene": "JSON decode error"},
    {"id": "I-07", "descripcion": "patente mal formada",
     "metodo": "GET", "ruta": "/ingresos/ABC",
     "estado": 422, "contiene": "patente"},
    {"id": "I-08", "descripcion": "patente sin ingreso hoy",
     "metodo": "GET", "ruta": "/ingresos/ZZZZ99",
     "estado": 404, "contiene": "no_encontrado"},
    {"id": "I-09", "descripcion": "metodo no permitido",
     "metodo": "GET", "ruta": "/consultas",
     "estado": 405, "contiene": "metodo_no_permitido"},
    {"id": "I-10", "descripcion": "ruta que no existe",
     "metodo": "GET", "ruta": "/ruta-inexistente",
     "estado": 404, "contiene": "no_encontrado"},
    {"id": "I-11", "descripcion": "guia demasiado corta",
     "metodo": "POST", "ruta": "/extracciones", "json": {"texto": "RUT 12.345.678-5"},
     "estado": 422, "contiene": "at least 20 characters"},
    {"id": "I-12", "descripcion": "guia de 2001 caracteres",
     "metodo": "POST", "ruta": "/extracciones", "json": {"texto": GUIA_LARGA},
     "estado": 422, "contiene": "at most 2000 characters"},
]


def ejecutar_caso(cliente, caso):
    """Envia el caso con cualquier cliente que tenga .request()."""
    if "contenido" in caso:
        r = cliente.request(
            caso["metodo"],
            caso["ruta"],
            content=caso["contenido"],
            headers={"Content-Type": "application/json"},
        )
    else:
        r = cliente.request(
            caso["metodo"], caso["ruta"], json=caso.get("json")
        )
    ok = r.status_code == caso["estado"] and caso["contiene"] in r.text
    return ok, r.status_code, r.text
