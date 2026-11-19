"""CRUD de tareas con filtros, paginación y escritura protegida por JWT."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Category, Project, Task, User
from app.schemas import (
    PaginatedResponse,
    TaskCreate,
    TaskRead,
    TaskUpdate,
)


router = APIRouter(prefix="/tasks", tags=["tasks"])

DatabaseSession = Annotated[Session, Depends(get_db)]
PositiveId = Annotated[int, Path(gt=0)]


def find_task(db: Session, task_id: int) -> Task:
    """Busca una tarea o devuelve un error 404."""
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada.",
        )

    return task


def validate_relations(db: Session, data: TaskCreate) -> None:
    """Comprueba que existen los registros relacionados."""
    if db.get(Project, data.project_id) is None:
        raise HTTPException(
            status_code=404,
            detail="El proyecto indicado no existe.",
        )

    if data.category_id is not None:
        if db.get(Category, data.category_id) is None:
            raise HTTPException(
                status_code=404,
                detail="La categoría indicada no existe.",
            )

    if data.assignee_id is not None:
        if db.get(User, data.assignee_id) is None:
            raise HTTPException(
                status_code=404,
                detail="El usuario asignado no existe.",
            )


def commit_changes(db: Session) -> None:
    """Confirma los cambios y gestiona conflictos de integridad."""
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=(
                "Conflicto de integridad al guardar los cambios. "
                "Comprueba que los registros relacionados siguen existiendo."
            ),
        ) from None


@router.get(
    "",
    response_model=PaginatedResponse[TaskRead],
    summary="Listar tareas",
)
def list_tasks(
    db: DatabaseSession,
    project_id: Annotated[int | None, Query(gt=0)] = None,
    completed: bool | None = None,
    category_id: Annotated[int | None, Query(gt=0)] = None,
    assignee_id: Annotated[int | None, Query(gt=0)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    sort_by: Literal["id", "title", "created_at"] = "id",
    order: Literal["asc", "desc"] = "asc",
):
    """Combina filtros y devuelve una página con el total de resultados."""
    filters = []

    if project_id is not None:
        filters.append(Task.project_id == project_id)

    if completed is not None:
        filters.append(Task.completed == completed)

    if category_id is not None:
        filters.append(Task.category_id == category_id)

    if assignee_id is not None:
        filters.append(Task.assignee_id == assignee_id)

    total = db.scalar(
        select(func.count())
        .select_from(Task)
        .where(*filters)
    )

    sort_columns = {
        "id": Task.id,
        "title": Task.title,
        "created_at": Task.created_at,
    }

    sort_column = sort_columns[sort_by]
    ordering = (
        sort_column.desc()
        if order == "desc"
        else sort_column.asc()
    )

    statement = (
        select(Task)
        .where(*filters)
        .order_by(ordering)
    )

    if sort_by != "id":
        statement = statement.order_by(Task.id.asc())

    statement = statement.offset(skip).limit(limit)

    return {
        "items": db.scalars(statement).all(),
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Consultar una tarea",
)
def get_task(
    task_id: PositiveId,
    db: DatabaseSession,
):
    return find_task(db, task_id)


@router.post(
    "",
    response_model=TaskRead,
    status_code=201,
    summary="Crear una tarea",
    dependencies=[Depends(get_current_user)],
)
def create_task(
    data: TaskCreate,
    db: DatabaseSession,
):
    """Requiere un usuario autenticado mediante JWT."""
    validate_relations(db, data)

    task = Task(
        **data.model_dump(),
        completed=False,
    )

    db.add(task)
    commit_changes(db)
    db.refresh(task)

    return task


@router.put(
    "/{task_id}",
    response_model=TaskRead,
    summary="Modificar una tarea",
    dependencies=[Depends(get_current_user)],
)
def update_task(
    task_id: PositiveId,
    data: TaskUpdate,
    db: DatabaseSession,
):
    """Requiere JWT y conserva el ID y la fecha de creación."""
    task = find_task(db, task_id)
    validate_relations(db, data)

    for field, value in data.model_dump().items():
        setattr(task, field, value)

    commit_changes(db)
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=204,
    response_class=Response,
    summary="Eliminar una tarea",
    dependencies=[Depends(get_current_user)],
)
def delete_task(
    task_id: PositiveId,
    db: DatabaseSession,
):
    """Requiere un usuario autenticado mediante JWT."""
    task = find_task(db, task_id)

    db.delete(task)
    commit_changes(db)

    return Response(status_code=204)