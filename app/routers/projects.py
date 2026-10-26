"""Rutas relacionadas con los proyectos de TaskFlow."""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas import ProjectCreate, ProjectRead


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectRead,
    status_code=201,
    summary="Crear un proyecto simulado",
    description=(
        "Valida los datos y devuelve un proyecto de ejemplo. "
        "No guarda información en una base de datos."
    ),
)
def create_project(project: ProjectCreate) -> ProjectRead:
    """Simula la creación de un proyecto sin persistencia."""
    return ProjectRead(
        **project.model_dump(),
        id=1,
        created_at=datetime.now(timezone.utc),
    )