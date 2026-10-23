import os
import requests
import json
import re

from dotenv import load_dotenv

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

#instrucciones es para que el asisten ia lea un texto donde un conductor transportiste indicara informacia de una guia
INSTRUCCIONES="eres un asistente de inteligencia artificial que ayuda a los transportistas a extraer información de guías de transporte. Tu tarea es leer el texto proporcionado por el conductor y extraer los datos relevantes de la guía, nombre del chofer, su rut, el número de guía, el nombre del remitente, el nombre del destinatario, la dirección de entrega y cualquier otra información importante. Devuelve los datos en formato JSON  dentro de items con las claves 'atributo' ,'valor' y 'calidad' (del 1 al 5 , indica la calidad del dato entregado) , y guardar la fecha de ejecucion de la peticion dentro de dateInput."
MODEL="gemini-3.8-flash"




load_dotenv()

 

    
def init_gemmini_model(pregunta):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("La clave API no puede estar vacía")
    url = "https://generativelanguage.googleapis.com/v1beta/interactions"
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    body={
        "model": MODEL,
        "system_instruction": INSTRUCCIONES,
        "input": pregunta
    }
    if response_schema is not None:
        body["response_format"] = {
            "type": "text",
            "mime_type": "application/json",
            "schema": response_schema
        }
    return url, headers,body 

def parsear_respuesta_json(texto):
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido.")
    if not isinstance(datos, dict) or "dateInput" not in datos or not isinstance(datos.get("items"), list) or not all(
        isinstance(item, dict) and "atributo" in item and "valor" in item and "calidad" in item
        for item in datos["items"]
    ):
        raise ValueError("La respuesta no tiene la estructura esperada.")
    return datos
    
def armar_peticion(pregunta):

    if MODEL.startswith("gemini"):
            return init_gemmini_model(pregunta) 
    else:
        raise ValueError(f"Modelo no soportado: {MODEL}")

def enviar_peticion(pregunta):
    url, headers, body = armar_peticion(pregunta)
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
    respuesta = enviar_peticion(pregunta)
    return extraer_texto(respuesta)

try:    
    _pregunta="mi nombre es juan perez y mi numero de guia es 123456789, con fecha 1000/10/2029, el remitente es juan perez y el destinatario es maria lopez, la direccion de entrega es calle falsa 123, ciudad de mexico" 
    print("pregunta :", _pregunta)
    resultado=obtener_dato_de_prueba(_pregunta) 
    print( resultado)
    jsonResult=parsear_respuesta_json(resultado);
    print(jsonResult)
except (ValueError, RuntimeError) as error:
     print("No se pudo completar la operación:", error)
