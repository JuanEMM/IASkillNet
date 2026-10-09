import os
import requests
from dotenv import load_dotenv
 
  
load_dotenv()
def armar_peticion(pregunta):
    _api_key = os.getenv("GEMINI_API_KEY")
    _modelo = "gemini-3.8-flash"
    _url = "https://generativelanguage.googleapis.com/v1beta/interactions"
    _headers={"Content-Type": "application/json", "x-goog-api-key": _api_key}
    _body =  pregunta
    return {"url": _url, "headers": _headers, "body": _body, "modelo": _modelo}
def enviar_peticion(url, headers, body, modelo):
    respuesta = requests.post(
                                url, 
                                headers=headers,
                                json={"model": modelo, "input": body},) 
    return respuesta.json()
def extraer_texto(respuesta):
    return respuesta["steps"][1]["content"][0]["text"]
def obtener_dato_de_prueba(pregunta):
    url, headers, body, modelo = armar_peticion(pregunta).values()
    respuesta = enviar_peticion(url, headers, body, modelo)
    return extraer_texto(respuesta)
# def obtener_dato_de_prueba(pregunta):
#      _api_key = os.getenv("GEMINI_API_KEY")
#      _modelo = "gemini-3.8-flash"
#      _url = "https://generativelanguage.googleapis.com/v1beta/interactions"
#      _headers={"Content-Type": "application/json", "x-goog-api-key": _api_key}
#      _body =  pregunta
#      respuesta = requests.post(
#                                 _url, 
#                                 headers=_headers,
#                                 json={"model": _modelo, "input": _body},)
#      datos = respuesta.json()
#      return datos["steps"][1]["content"][0]["text"]
print(obtener_dato_de_prueba("que dia es hoy?"))
