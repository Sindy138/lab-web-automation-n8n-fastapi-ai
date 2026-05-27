import os
import uuid
from typing import Optional

from groq import Groq
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

tareas_db: list[dict] = []

USUARIOS_MOCK = {
    1:  {"id": 1,  "nombre": "Ana García",    "email": "ana@example.com",    "plan": "premium"},
    2:  {"id": 2,  "nombre": "Luis Martínez", "email": "luis@example.com",   "plan": "basic"},
    42: {"id": 42, "nombre": "Carlos López",  "email": "carlos@example.com", "plan": "premium"},
}


class TareaEntrada(BaseModel):
    titulo: str
    prioridad: str
    descripcion: str = ""


class ChatRequest(BaseModel):
    message: str


@app.post("/tareas", status_code=201)
def crear_tarea(tarea: TareaEntrada):
    nueva = {
        "id": str(uuid.uuid4()),
        "titulo": tarea.titulo,
        "prioridad": tarea.prioridad,
        "descripcion": tarea.descripcion,
        "completada": False,
    }
    tareas_db.append(nueva)
    return nueva


@app.get("/tareas")
def listar_tareas(completada: Optional[bool] = None):
    if completada is None:
        return tareas_db
    return [t for t in tareas_db if t["completada"] == completada]


@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    usuario = USUARIOS_MOCK.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@app.post("/api/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY no configurada en .env")
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[{"role": "user", "content": request.message}],
    )
    return {"respuesta": completion.choices[0].message.content}
