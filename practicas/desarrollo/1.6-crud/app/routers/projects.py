"""CRUD de proyectos, tareas asociadas y contadores."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy import case, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Project, Task
from app.schemas import (
    PaginatedResponse,
    ProjectCreate,
    ProjectDetail,
    ProjectRead,
    ProjectSummary,
    ProjectUpdate,
)


router = APIRouter(prefix="/projects", tags=["projects"])

DatabaseSession = Annotated[Session, Depends(get_db)]
PositiveId = Annotated[int, Path(gt=0)]


def find_project(db: Session, project_id: int) -> Project:
    """Busca un proyecto o devuelve un error 404."""

    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado.",
        )

    return project


def commit_changes(db: Session) -> None:
    """Confirma la transacción y gestiona conflictos de integridad."""

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo completar la operación por un conflicto de integridad.",
        ) from None


@router.get(
    "",
    response_model=PaginatedResponse[ProjectRead],
    summary="Listar proyectos",
)
def list_projects(
    db: DatabaseSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    sort_by: Literal["id", "name", "created_at"] = "id",
    order: Literal["asc", "desc"] = "asc",
):
    """Devuelve una página de proyectos con el total de registros."""

    total = db.scalar(
        select(func.count()).select_from(Project)
    )

    sort_columns = {
        "id": Project.id,
        "name": Project.name,
        "created_at": Project.created_at,
    }
    sort_column = sort_columns[sort_by]
    ordering = (
        sort_column.desc()
        if order == "desc"
        else sort_column.asc()
    )

    statement = select(Project).order_by(ordering)

    if sort_by != "id":
        statement = statement.order_by(Project.id.asc())

    statement = statement.offset(skip).limit(limit)

    return {
        "items": db.scalars(statement).all(),
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get(
    "/{project_id}/summary",
    response_model=ProjectSummary,
    summary="Consultar contadores de un proyecto",
)
def get_project_summary(
    project_id: PositiveId,
    db: DatabaseSession,
):
    """Calcula los contadores en SQL sin cargar todas las tareas."""

    project = find_project(db, project_id)

    statement = (
        select(
            func.count(Task.id),
            func.coalesce(
                func.sum(
                    case(
                        (Task.completed.is_(True), 1),
                        else_=0,
                    )
                ),
                0,
            ),
        )
        .where(Task.project_id == project_id)
    )

    total_tasks, completed_tasks = db.execute(statement).one()

    return {
        **ProjectRead.model_validate(project).model_dump(),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks,
    }


@router.get(
    "/{project_id}",
    response_model=ProjectDetail,
    summary="Consultar un proyecto con sus tareas",
)
def get_project(
    project_id: PositiveId,
    db: DatabaseSession,
):
    """Carga el proyecto y su colección de tareas."""

    statement = (
        select(Project)
        .where(Project.id == project_id)
        .options(selectinload(Project.tasks))
    )

    project = db.scalar(statement)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado.",
        )

    return project


@router.post(
    "",
    response_model=ProjectRead,
    status_code=201,
    summary="Crear un proyecto",
)
def create_project(
    data: ProjectCreate,
    db: DatabaseSession,
):
    project = Project(**data.model_dump())

    db.add(project)
    commit_changes(db)
    db.refresh(project)

    return project


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Modificar un proyecto",
)
def update_project(
    project_id: PositiveId,
    data: ProjectUpdate,
    db: DatabaseSession,
):
    """Actualiza nombre y descripción conservando sus tareas."""

    project = find_project(db, project_id)

    for field, value in data.model_dump().items():
        setattr(project, field, value)

    commit_changes(db)
    db.refresh(project)

    return project


@router.delete(
    "/{project_id}",
    status_code=204,
    response_class=Response,
    summary="Eliminar un proyecto y sus tareas",
)
def delete_project(
    project_id: PositiveId,
    db: DatabaseSession,
):
    """Elimina el proyecto y aplica la cascada definida en los modelos."""

    project = find_project(db, project_id)

    db.delete(project)
    commit_changes(db)

    return Response(status_code=204)