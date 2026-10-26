"""Configuración principal y registro de routers de TaskFlow."""

from fastapi import FastAPI

from app.routers import projects, status, tasks


tags_metadata = [
    {
        "name": "tasks",
        "description": "Operaciones de tareas. La creación es simulada.",
    },
    {
        "name": "projects",
        "description": "Operaciones de proyectos. La creación es simulada.",
    },
    {
        "name": "status",
        "description": "Comprobaciones de salud, versión y conectividad.",
    },
]


app = FastAPI(
    title="TaskFlow API",
    description="API de gestión de tareas y proyectos organizada por recursos.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)


app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(status.router)