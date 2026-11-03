"""Rutas relacionadas con las tareas de TaskFlow."""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas import TaskCreate, TaskRead


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskRead,
    status_code=201,
    summary="Crear una tarea simulada",
    description=(
        "Valida los datos y devuelve una tarea de ejemplo. "
        "No guarda información en una base de datos."
    ),
)
def create_task(task: TaskCreate) -> TaskRead:
    """Simula la creación de una tarea sin persistencia."""
    return TaskRead(
        **task.model_dump(),
        id=1,
        completed=False,
        created_at=datetime.now(timezone.utc),
    )