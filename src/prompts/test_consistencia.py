import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.consumir_gemini import enviar_peticion, extraer_texto, parsear_respuesta_json
from src.prompts.banco import BANCO_DE_PROMPTS

RUTA_REGISTRO = os.path.join(os.path.dirname(__file__), "registro_resultados.json")

registro = {}

for prompt in BANCO_DE_PROMPTS:
    exitos = 0
    intentos = 3
    for intento in range(intentos):
        try:
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
        time.sleep(1)
    print(f"{prompt['nombre']}: {exitos}/{intentos} respuestas válidas")
    registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}

with open(RUTA_REGISTRO, "w", encoding="utf-8") as archivo:
    json.dump(registro, archivo, indent=2, ensure_ascii=False)
