import os
import requests
import time

from dotenv import load_dotenv


load_dotenv()

# Tope de tokens de salida: sin él OpenRouter reserva el máximo del modelo (65536) y exige saldo para eso
_max_tokens = 1500
_pregunta="Indica tu fecha de actualización. Consulta el clima a esa fecha en Concepción, Chile. Explica tus limitaciones y desventajas para un proyecto que extraiga datos de facturas y guías de despacho desde imágenes JPG/PNG, incluyendo precisión OCR, formatos, costos, privacidad e integración."
def armar_peticion(pregunta):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    _api_key = os.getenv("OPENROUTER_API_KEY")
    if not _api_key:
        raise ValueError("La clave API no puede estar vacía")
    _modelo = "x-ai/grok-4.7"
    _url = "https://openrouter.ai/api/v1/chat/completions"
    _headers={"Content-Type": "application/json", "Authorization": f"Bearer {_api_key}"}
    _body =  pregunta
    return {"url": _url, "headers": _headers, "body": _body, "modelo": _modelo}
def enviar_peticion(url, headers, body, modelo):
    try:
        respuesta = requests.post(
                                    url,
                                    headers=headers,
                                    json={"model": modelo, "messages": [{"role": "user", "content": body}], "max_tokens": _max_tokens},)
        #print("Respuesta del servicio:", respuesta.text)  # Agrega esta línea para imprimir la respuesta completa
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")

def extraer_texto(respuesta):
    try:
        return respuesta["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")

def calcular_costo(respuesta, precio_entrada, precio_salida):
    uso = respuesta["usage"]
    tokens_entrada = uso["prompt_tokens"]
    tokens_salida = uso["completion_tokens"]
    return (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida)

def obtener_dato_de_prueba(pregunta):
    url, headers, body, modelo = armar_peticion(pregunta).values()
    respuesta = enviar_peticion(url, headers, body, modelo)
    return extraer_texto(respuesta), respuesta

try:
    # USD por token de grok-4.7 vía OpenRouter ($2 entrada / $6 salida por 1M de tokens)
    PRECIO_ENTRADA = 0.000002
    PRECIO_SALIDA = 0.000006
    print("pregunta :", _pregunta)
    latencias = []
    for i in range(4):
        inicio = time.perf_counter()
        resultado , respuesta = obtener_dato_de_prueba(_pregunta)
        fin = time.perf_counter()
        latencias.append(fin - inicio)
        print(f"Intento {i + 1}: {latencias[-1]:.2f} segundos")
    latencia_promedio = sum(latencias) / len(latencias)
    print(f"Latencia promedio: {latencia_promedio:.2f} segundos")

    costo = calcular_costo(respuesta, PRECIO_ENTRADA, PRECIO_SALIDA)
    print(f"Costo de la última petición: {costo}")
    print(resultado)
except (ValueError, RuntimeError) as error:
     print("No se pudo completar la operación:", error)
