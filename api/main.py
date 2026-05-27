from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

tareas = []


class Tarea(BaseModel):
    titulo: str
    prioridad: str


@app.post("/tareas", status_code=201)
def crear_tarea(tarea: Tarea):
    nueva = {
        "id": str(uuid.uuid4()),
        "titulo": tarea.titulo,
        "prioridad": tarea.prioridad,
    }
    tareas.append(nueva)
    return nueva


@app.get("/tareas")
def listar_tareas():
    return tareas
