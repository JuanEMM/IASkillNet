import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.8-flash"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"

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
        json={"model": MODEL, "input": datos.prompt},
        timeout=30,
    )
    if not respuesta.ok:
        raise HTTPException(status_code=respuesta.status_code, detail=respuesta.text)

    # La respuesta trae "steps"; el texto está en los pasos de tipo "model_output"
    texto = "".join(
        parte.get("text", "")
        for paso in respuesta.json().get("steps", [])
        if paso.get("type") == "model_output"
        for parte in paso.get("content", [])
        if parte.get("type") == "text"
    )
    return {"respuesta": texto}
