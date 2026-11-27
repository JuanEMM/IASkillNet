"""Verifica el servicio contra los criterios de aceptacion de la ficha (Bloque 35).

Uso, desde la raiz del repositorio:
    python src/verificar_servicio.py
DOC-1 y DOC-2 no llaman al modelo. CA-01 a CA-06 usan Gemini (GEMINI_API_KEY en .env y
conexion): son 4 llamadas, porque los criterios que envian lo mismo reutilizan la respuesta.
Termina con codigo 0 si todo se cumple y con 1 si algo falla.
"""
from functools import lru_cache

from fastapi.testclient import TestClient

from servicio import logica
from servicio.esquemas import GUIA_EJEMPLO
from servicio.main import app

cliente = TestClient(app)

# Guias de prueba de la ficha: G-01 es valida; G-02 es igual pero con el digito verificador del RUT malo
G01 = GUIA_EJEMPLO
G02 = GUIA_EJEMPLO.replace("12.345.678-5", "12.345.678-9")
PREGUNTA_PATENTE = "cuando ingreso el camion BXKL45"
PREGUNTA_FUERA = "cual es el horario del casino de la planta"
MODELOS = ("Consulta", "Item", "RespuestaConsulta", "Guia", "DatoGuia", "RespuestaExtraccion")


def esquema():
    return cliente.get("/openapi.json").json()


@lru_cache
def extraer(texto):
    r = cliente.post("/extracciones", json={"texto": texto})
    return r.status_code, r.json()


@lru_cache
def consultar(pregunta):
    r = cliente.post("/consultas", json={"pregunta": pregunta})
    return r.status_code, r.json()


def dato(items, es_el_dato):
    return next((i for i in items if es_el_dato(i["atributo"])), None)


def docs_navegables():
    r = cliente.get("/docs")
    if r.status_code != 200:
        return False, f"/docs responde {r.status_code}"
    return True, f"rutas documentadas: {sorted(esquema()['paths'])}"


def campos_documentados():
    esquemas = esquema()["components"]["schemas"]
    sin = [
        f"{nombre}.{campo}"
        for nombre in MODELOS
        for campo, datos in esquemas[nombre]["properties"].items()
        if "description" not in datos
    ]
    if sin:
        return False, f"sin descripcion: {sin}"
    return True, "todos los campos tienen descripcion"


def ca_01():
    estado, datos = extraer(G01)
    items = datos.get("items", [])
    ok = (
        estado == 200
        and "dateInput" in datos
        and len(items) > 0
        and all(i["atributo"] and i["valor"] and 1 <= i["calidad"] <= 5 for i in items)
    )
    return ok, f"estado {estado}, {len(items)} items, campos {sorted(datos)}"


def ca_02():
    _, datos = extraer(G01)
    rut = dato(datos["items"], logica.es_rut)
    patente = dato(datos["items"], logica.es_patente)
    ok = bool(rut and patente) and not rut["requiere_confirmacion"] and not patente["requiere_confirmacion"]
    return ok, (
        f"RUT {rut and rut['valor']} -> {rut and rut['requiere_confirmacion']}, "
        f"patente {patente and patente['valor']} -> {patente and patente['requiere_confirmacion']}"
    )


def ca_03():
    _, datos = extraer(G02)
    rut = dato(datos["items"], logica.es_rut)
    ok = bool(rut) and rut["requiere_confirmacion"]
    return ok, f"RUT {rut and rut['valor']} -> requiere_confirmacion {rut and rut['requiere_confirmacion']}"


def ca_04():
    estado, datos = consultar(PREGUNTA_PATENTE)
    ok = estado == 200 and {"trace_id", "items"} <= set(datos)
    return ok, f"estado {estado}, campos {sorted(datos)}"


def ca_05():
    _, datos = consultar(PREGUNTA_PATENTE)
    citas = [i for i in datos["items"] if i["fuente"] == "ingreso-0007"]
    ok = any("07:40" in i["valor"] for i in citas)
    return ok, f"fuentes citadas: {sorted({i['fuente'] for i in datos['items']})}"


def ca_06():
    _, datos = consultar(PREGUNTA_FUERA)
    return datos["items"] == [], f"items: {datos['items']}"


COMPROBACIONES = [
    ("DOC-1", "documentacion en /docs", docs_navegables),
    ("DOC-2", "campos documentados", campos_documentados),
    ("CA-01", "extraccion con dateInput e items de calidad 1 a 5", ca_01),
    ("CA-02", "RUT y patente validos no piden confirmacion", ca_02),
    ("CA-03", "RUT con digito verificador malo pide confirmacion", ca_03),
    ("CA-04", "consulta con trace_id e items", ca_04),
    ("CA-05", "BXKL45 citado desde ingreso-0007 a las 07:40", ca_05),
    ("CA-06", "pregunta fuera de los documentos: items vacio", ca_06),
]


def ejecutar(comprobaciones):
    cumplidas = 0
    for id_, descripcion, prueba in comprobaciones:
        try:
            ok, evidencia = prueba()
        except Exception as error:
            ok = False
            evidencia = f"error: {type(error).__name__}({error})"
        estado = "PASA " if ok else "FALLA"
        print(f"{estado} {id_} {descripcion} -> {evidencia}")
        cumplidas += 1 if ok else 0
    print(
        f"\n{cumplidas} de {len(comprobaciones)} comprobaciones cumplidas"
    )
    return cumplidas == len(comprobaciones)


if __name__ == "__main__":
    raise SystemExit(0 if ejecutar(COMPROBACIONES) else 1)
