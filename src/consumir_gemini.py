import os
import requests
from dotenv import load_dotenv
 
  
load_dotenv()
  
def obtener_dato_de_prueba(pregunta):
     _api_key = os.getenv("GEMINI_API_KEY")
     _modelo = "gemini-3.8-flash"
     _url = "https://generativelanguage.googleapis.com/v1beta/interactions"
     _headers={"Content-Type": "application/json", "x-goog-api-key": _api_key}
     _body =  pregunta
     respuesta = requests.post(
                                _url, 
                                headers=_headers,
                                json={"model": _modelo, "input": _body},)
     datos = respuesta.json()
     return datos["steps"][1]["content"][0]["text"]
print(obtener_dato_de_prueba("que dia es hoy?"))
