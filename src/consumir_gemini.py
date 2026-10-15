import os
import requests
import time

from dotenv import load_dotenv

_pregunta="Indica tu fecha de actualización. Consulta el clima a esa fecha en Concepción, Chile. Explica tus limitaciones y desventajas para un proyecto que extraiga datos de facturas y guías de despacho desde imágenes JPG/PNG, incluyendo precisión OCR, formatos, costos, privacidad e integración."

load_dotenv()

# Reintentos ante saturación del servicio: la espera se duplica en cada intento (5, 10, 20, 40 s)
_max_reintentos = 5
_espera_base = 5

class ServicioNoDisponible(RuntimeError):
    pass

def armar_peticion(pregunta):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    _api_key = os.getenv("GEMINI_API_KEY")
    if not _api_key:
        raise ValueError("La clave API no puede estar vacía")
    _modelo = "gemini-2.5-flash"
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
        #print("Respuesta del servicio:", respuesta.text)  # Agrega esta línea para imprimir la respuesta completa
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos segundos.")
    try:
        datos = respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")
    if datos.get("error", {}).get("code") == "service_unavailable":
        raise ServicioNoDisponible("El servicio está saturado en este momento.")
    if "error" in datos:
        raise RuntimeError(f"El servicio rechazó la petición: {datos['error'].get('message', datos['error'])}")
    return datos

def extraer_texto(respuesta):
    try:
        return respuesta["steps"][1]["content"][0]["text"]
    except (KeyError, IndexError):
     	raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")

def calcular_costo(respuesta, precio_entrada, precio_salida):
	uso = respuesta["usage"]
	tokens_entrada = uso["total_input_tokens"]
	tokens_salida = uso["total_output_tokens"] + uso.get("total_thought_tokens", 0)
	return (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida)

def obtener_dato_de_prueba(pregunta):
    url, headers, body, modelo = armar_peticion(pregunta).values() 
    respuesta = enviar_peticion(url, headers, body, modelo) 
    return extraer_texto(respuesta), respuesta

def obtener_dato_con_reintentos(pregunta):
    for reintento in range(_max_reintentos):
        inicio = time.perf_counter()
        try:
            resultado, respuesta = obtener_dato_de_prueba(pregunta)
        except ServicioNoDisponible:
            if reintento == _max_reintentos - 1:
                raise
            espera = _espera_base * 2 ** reintento
            #print(f"Servicio saturado, reintentando en {espera} segundos ({reintento + 1}/{_max_reintentos - 1})")
            time.sleep(espera)
        else:
            # La latencia cuenta solo la petición exitosa, sin las esperas entre reintentos
            return resultado, respuesta, time.perf_counter() - inicio

try:
    # USD por token de gemini-2.5-flash ($0.30 entrada / $2.50 salida por 1M de tokens; el razonamiento se cobra como salida)
    PRECIO_ENTRADA = 0.0000003 
    PRECIO_SALIDA = 0.0000025 
    latencias = []
    print("pregunta :", _pregunta)
    for i in range(4):        
        resultado , respuesta, latencia = obtener_dato_con_reintentos(_pregunta)
        latencias.append(latencia)
        print(f"Intento {i + 1}: {latencias[-1]:.2f} segundos")    
    latencia_promedio = sum(latencias) / len(latencias)
    print(f"Latencia promedio: {latencia_promedio:.2f} segundos")
    
    costo = calcular_costo(respuesta, PRECIO_ENTRADA, PRECIO_SALIDA)
    print(f"Costo de la última petición: {costo}") 
    print(resultado) 
except (ValueError, RuntimeError) as error:
     print("No se pudo completar la operación:", error)
