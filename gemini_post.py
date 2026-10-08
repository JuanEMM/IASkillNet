import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def generar(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError("Falta GEMINI_API_KEY en el archivo .env")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    body = {"contents": [{"parts": [{"text": prompt}]}]}

    respuesta = requests.post(URL, headers=headers, json=body, timeout=30)
    respuesta.raise_for_status()

    datos = respuesta.json()
    return datos["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "Explica en una frase qué es una API."
    try:
        print(generar(prompt))
    except requests.HTTPError as e:
        print(f"Error HTTP {e.response.status_code}: {e.response.text}")
    except RuntimeError as e:
        print(e)
