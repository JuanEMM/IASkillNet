import os
import requests
from dotenv import load_dotenv
 
  
load_dotenv()
def armar_peticion(pregunta):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    _api_key = os.getenv("GEMINI_API_KEY")
    if not _api_key:
        raise ValueError("La clave API no puede estar vacía")
    _modelo = "gemini-3.8-flash"
    _url = "https://generativelanguage.googleapis.com/v1beta/interactions"
    _headers={"Content-Type": "application/json", "x-goog-api-key": _api_key}
    _body =  pregunta
    return {"url": _url, "headers": _headers, "body": _body, "modelo": _modelo}
def enviar_peticion(url, headers, body, modelo):
    try:
        respuesta = requests.post(
                                    url, 
                                    headers=headers,
                                    json={"model": modelo, "input": body},) 
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")
def extraer_texto(respuesta):
    try:
        return respuesta["steps"][1]["content"][0]["text"]
    except (KeyError, IndexError):
     	raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")
def obtener_dato_de_prueba(pregunta):
    url, headers, body, modelo = armar_peticion(pregunta).values()
    respuesta = enviar_peticion(url, headers, body, modelo)
    return extraer_texto(respuesta) 


try:
     resultado = obtener_dato_de_prueba("Sí, esta conexión funciona correctamente.")
     print(resultado)
except (ValueError, RuntimeError) as error:
     print("No se pudo completar la operación:", error)
