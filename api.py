import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

app = FastAPI(title="Prueba API key Gemini")


class Consulta(BaseModel):
    prompt: str


@app.post("/consulta")
def consulta(datos: Consulta):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Falta GEMINI_API_KEY en el archivo .env")

    respuesta = requests.post(
        GEMINI_URL,
        headers={"Content-Type": "application/json", "x-goog-api-key": API_KEY},
        json={"contents": [{"parts": [{"text": datos.prompt}]}]},
        timeout=30,
    )
    if not respuesta.ok:
        raise HTTPException(status_code=respuesta.status_code, detail=respuesta.text)

    texto = respuesta.json()["candidates"][0]["content"]["parts"][0]["text"]
    return {"respuesta": texto}
