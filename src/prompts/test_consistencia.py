"""Prueba de consistencia del banco de prompts.

Por cada prompt de BANCO_DE_PROMPTS envía su ejemplo_usuario 3 veces y cuenta
cuántas respuestas son JSON válido con las claves esperadas. Imprime el
resultado de cada prompt y lo guarda en registro_resultados.json (junto a este
archivo; se sobrescribe en cada corrida).

Hace llamadas reales a la API: 3 prompts x 3 intentos.
Se ejecuta con: python src/prompts/test_consistencia.py
"""
import json
import os
import sys
import time

# Agrega la raíz del proyecto al path. Si se ejecuta este archivo directo, Python solo
# agrega src/prompts/ y el "from src..." de abajo no encontraría el paquete.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.consumir_gemini import enviar_peticion, extraer_texto, parsear_respuesta_json
from src.prompts.banco import BANCO_DE_PROMPTS

# el registro se guarda al lado de este archivo, sin importar desde dónde se ejecute
RUTA_REGISTRO = os.path.join(os.path.dirname(__file__), "registro_resultados.json")

# nombre del prompt -> {"exitos": n, "intentos": n}
registro = {}

for prompt in BANCO_DE_PROMPTS:
    exitos = 0
    intentos = 3
    for intento in range(intentos):
        try:
            # un intento es éxito solo si la petición no falla y la respuesta pasa la
            # validación; cualquier error se muestra y se sigue con el siguiente intento
            respuesta = enviar_peticion(
                prompt["ejemplo_usuario"],
                prompt["system_instruction"],
                prompt.get("response_schema"),
            )
            texto = extraer_texto(respuesta)
            parsear_respuesta_json(texto, prompt["claves_esperadas"])
            exitos += 1
        except (ValueError, RuntimeError) as error:
            print(f"  intento {intento + 1} falló: {error}")
        # pausa corta entre intentos para no saturar la API
        time.sleep(1)
    print(f"{prompt['nombre']}: {exitos}/{intentos} respuestas válidas")
    registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}

with open(RUTA_REGISTRO, "w", encoding="utf-8") as archivo:
    json.dump(registro, archivo, indent=2, ensure_ascii=False)
