
from datetime import datetime, timezone

from app.schemas import TaskCreate, TaskRead


from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


app = FastAPI(
    title="TaskFlow API",
    description="API inicial del proyecto TaskFlow para gestionar tareas.",
    version="1.0.0"
)


@app.get(
    "/health",
    summary="Comprobar el estado de la API",
    description="Comprueba que el servidor de TaskFlow está funcionando correctamente.",
    response_model=HealthResponse
)
def health():
    return {"status": "ok"}


@app.get(
    "/version",
    summary="Consultar la versión de la API",
    description="Devuelve la versión actual de la API de TaskFlow."
)
def version():
    return {"version": "1.0.0"}


@app.get(
    "/ping",
    summary="Comprobar la conectividad",
    description="Endpoint sencillo para comprobar que la API responde."
)
def ping():
    return {"message": "pong"}  

@app.post(
    "/tasks",
    response_model=TaskRead,
    status_code=201,
    summary="Crear una tarea simulada",
    description=(
        "Valida los datos de entrada y devuelve una tarea de ejemplo. "
        "No guarda información en una base de datos."
    ),
    tags=["Tareas"],
)
def create_task(task: TaskCreate) -> TaskRead:
    """Simula la creación de una tarea sin persistencia."""
    return TaskRead(
        **task.model_dump(),
        id=1,
        completed=False,
        created_at=datetime.now(timezone.utc),
    )