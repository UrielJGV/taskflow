"""Rutas de tareas con persistencia en SQLite."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, Task
from app.schemas import TaskCreate, TaskRead


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una tarea",
)
def create_task(
    task: TaskCreate,
    db: DatabaseSession,
):
    """Guarda una tarea asociada a un proyecto existente."""

    project = db.get(Project, task.project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El proyecto indicado no existe.",
        )

    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
    )

    db.add(new_task)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la tarea. Comprueba su proyecto.",
        ) from None

    db.refresh(new_task)

    return new_task


@router.get(
    "",
    response_model=list[TaskRead],
    summary="Listar tareas",
)
def list_tasks(
    db: DatabaseSession,
    project_id: Annotated[int | None, Query(gt=0)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """Consulta tareas y permite filtrarlas por proyecto."""

    statement = select(Task)

    if project_id is not None:
        statement = statement.where(Task.project_id == project_id)

    statement = (
        statement
        .order_by(Task.id)
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Consultar una tarea",
)
def get_task(
    task_id: Annotated[int, Path(gt=0)],
    db: DatabaseSession,
):
    """Busca una tarea y devuelve 404 si no existe."""

    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada.",
        )

    return task