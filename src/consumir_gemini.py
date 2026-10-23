"""Cliente de Gemini para la miniaplicación de guías de transporte.

Arma la petición, la envía, saca el texto de la respuesta y valida que sea el
JSON que se le pidió al modelo. Por defecto usa el prompt de guías
(INSTRUCCIONES y response_schema); para otro prompt del banco se pasan por
parámetro. Ejecutado directo hace una consulta de ejemplo.
"""
import os
import requests
import json
import re

from dotenv import load_dotenv

# Forma del JSON que se le exige al modelo con el prompt de guías (es la misma de prompts/banco.py)
response_schema = {
    "type": "object",
    "properties": {
        "dateInput": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "atributo": {"type": "string"},
                    "valor": {"type": "string"},
                    "calidad": {"type": "number"}
                },
                "required": ["atributo", "valor", "calidad"]
            }
        }
    },
    "required": ["dateInput", "items"]
}

# Instrucción de sistema del prompt de guías; el mismo texto está en prompts/banco.py (obtener_datos_guia)
INSTRUCCIONES="eres un asistente de inteligencia artificial que ayuda a los transportistas a extraer información de guías de transporte. Tu tarea es leer el texto proporcionado por el conductor y extraer los datos relevantes de la guía, nombre del chofer, su rut, el número de guía, el nombre del remitente, el nombre del destinatario, la dirección de entrega y cualquier otra información importante. Devuelve los datos en formato JSON  dentro de items con las claves 'atributo' ,'valor' y 'calidad' (del 1 al 5 , indica la calidad del dato entregado) , y guardar la fecha de ejecucion de la peticion dentro de dateInput."
# Modelo que se consulta. armar_peticion solo acepta nombres que empiecen con "gemini"
MODEL="gemini-3.5-flash-lite"




load_dotenv()

 

    
def init_gemmini_model(pregunta, system_instruction=INSTRUCCIONES, schema=response_schema):
    """Arma lo necesario para llamar a Gemini.

    Recibe:
        pregunta: texto que se le envía al modelo.
        system_instruction: instrucción de sistema (por defecto la del prompt de guías).
        schema: esquema JSON que debe cumplir la respuesta; si es None, responde texto libre.
    Devuelve:
        tupla (url, headers, body), lista para usar en requests.post.
    Lanza ValueError si no está GEMINI_API_KEY en el .env.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("La clave API no puede estar vacía")
    # endpoint de interacciones (v1beta); el texto viene en "steps", ver extraer_texto
    url = "https://generativelanguage.googleapis.com/v1beta/interactions"
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    body={
        "model": MODEL,
        "system_instruction": system_instruction,
        "input": pregunta
    }
    # sin schema el modelo responde texto libre
    if schema is not None:
        body["response_format"] = {
            "type": "text",
            "mime_type": "application/json",
            "schema": schema
        }
    return url, headers,body

def parsear_respuesta_json(texto, claves_esperadas=("dateInput", "items")):
    """Convierte el texto que respondió el modelo en un dict y revisa su estructura.

    Recibe:
        texto: respuesta del modelo como string (puede venir dentro de un bloque ```json).
        claves_esperadas: claves que deben estar en el primer nivel del JSON.
    Devuelve:
        dict con los datos ya convertidos.
    Lanza ValueError si no es JSON válido, si falta alguna clave o si algún
    elemento de "items" no trae atributo, valor y calidad. Solo comprueba que
    las claves existan, no sus tipos.
    """
    # a veces el modelo envuelve el JSON en un bloque ```json ... ```; se lo sacamos
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido.")
    if not isinstance(datos, dict) or not all(clave in datos for clave in claves_esperadas):
        raise ValueError("La respuesta no tiene la estructura esperada.")
    # la forma de cada elemento de items está fija (atributo, valor, calidad)
    if "items" in datos and (not isinstance(datos["items"], list) or not all(
        isinstance(item, dict) and "atributo" in item and "valor" in item and "calidad" in item
        for item in datos["items"]
    )):
        raise ValueError("La respuesta no tiene la estructura esperada.")
    return datos

def armar_peticion(pregunta, system_instruction=INSTRUCCIONES, schema=response_schema):
    """Elige el proveedor según MODEL y arma la petición. Por ahora solo hay Gemini.

    Recibe:
        pregunta, system_instruction, schema: los mismos que init_gemmini_model.
    Devuelve:
        tupla (url, headers, body).
    Lanza ValueError si MODEL no es un modelo de Gemini.
    """

    if MODEL.startswith("gemini"):
            return init_gemmini_model(pregunta, system_instruction, schema)
    else:
        raise ValueError(f"Modelo no soportado: {MODEL}")

def enviar_peticion(pregunta, system_instruction=INSTRUCCIONES, schema=response_schema):
    """Envía la pregunta al modelo y devuelve lo que respondió el servicio.

    Recibe:
        pregunta, system_instruction, schema: los mismos que armar_peticion.
    Devuelve:
        dict con la respuesta completa del servicio (todavía sin sacarle el texto).
    Lanza RuntimeError si no hay conexión, si la respuesta no es JSON o si el
    servicio devuelve un error.
    """
    url, headers, body = armar_peticion(pregunta, system_instruction, schema)
    try:
        respuesta = requests.post(
                                    url, 
                                    headers=headers,
                                    json=body) 
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")
    try:
        datos = respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")
    if "error" in datos:
        raise RuntimeError(f"El servicio rechazó la petición: {datos['error'].get('message', datos['error'])}")
    return datos

def extraer_texto(respuesta):
    """Saca el texto generado de la respuesta del servicio.

    Recibe:
        respuesta: el dict que devuelve enviar_peticion.
    Devuelve:
        string con el texto del modelo. La API entrega una lista de "steps" y
        lo que generó el modelo está en los de tipo "model_output"; aquí se juntan.
    Lanza RuntimeError si no encuentra texto.
    """
    texto = "".join(
        parte.get("text", "")
        for paso in respuesta.get("steps", [])
        if paso.get("type") == "model_output"
        for parte in paso.get("content", [])
        if parte.get("type") == "text"
    )
    if not texto:
        raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")
    return texto

def obtener_dato_de_prueba(pregunta):     
    """Atajo para probar el flujo completo con el prompt por defecto.

    Recibe:
        pregunta: texto del conductor.
    Devuelve:
        string con lo que respondió el modelo, sin parsear.
    """
    respuesta = enviar_peticion(pregunta)
    return extraer_texto(respuesta)

# Esta condición solo se cumple cuando el archivo se ejecuta directo
# (python src/consumir_gemini.py). Si otro módulo lo importa, __name__ vale
# "src.consumir_gemini" y el bloque no corre. Así se puede importar las funciones
# (por ejemplo desde prompts/test_consistencia.py) sin disparar una llamada
# real a la API, y a la vez dejar acá una prueba rápida para hacer a mano.
if __name__ == "__main__":
    try:
        _pregunta="mi nombre es juan perez y mi numero de guia es 123456789, con fecha 1000/10/2029, el remitente es juan perez y el destinatario es maria lopez, la direccion de entrega es calle falsa 123, ciudad de mexico"
        print("pregunta :", _pregunta)
        resultado=obtener_dato_de_prueba(_pregunta)
        jsonResult=parsear_respuesta_json(resultado);
        print(jsonResult)
    except (ValueError, RuntimeError) as error:
         print("No se pudo completar la operación:", error)
