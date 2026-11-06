"""Rutas de proyectos con persistencia en SQLite."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectRead


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un proyecto",
)
def create_project(
    project: ProjectCreate,
    db: DatabaseSession,
):
    """Guarda un proyecto y devuelve sus datos definitivos."""

    new_project = Project(
        name=project.name,
        description=project.description,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get(
    "",
    response_model=list[ProjectRead],
    summary="Listar proyectos",
)
def list_projects(
    db: DatabaseSession,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """Consulta proyectos ordenados por identificador."""

    statement = (
        select(Project)
        .order_by(Project.id)
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Consultar un proyecto",
)
def get_project(
    project_id: Annotated[int, Path(gt=0)],
    db: DatabaseSession,
):
    """Busca un proyecto y devuelve 404 si no existe."""

    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado.",
        )

    return project