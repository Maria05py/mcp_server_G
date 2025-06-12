from fastapi import FastAPI
from pydantic import BaseModel
import requests

# Cargar el prompt maestro desde un archivo externo
with open("prompt.txt", "r", encoding="utf-8") as f:
    PROMPT_MAESTRO = f.read()

app = FastAPI()

API_KEY = "TU_API_KEY_DE_GEMINI"  # <-- Reemplazar con tu clave
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# Modelo de entrada
class Instruccion(BaseModel):
    mensaje: str

@app.post("/code")
def generar_codigo(data: Instruccion):
    # Combinar el prompt maestro con el mensaje del usuario
    prompt = f"{PROMPT_MAESTRO}\n\nInstrucción del usuario: {data.mensaje}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1024}
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(ENDPOINT, headers=headers, json=payload)

    if r.status_code == 200:
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return {"respuesta": text}
    else:
        return {"error": r.text}
