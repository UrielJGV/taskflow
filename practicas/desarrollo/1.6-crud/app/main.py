"""Configuración de TaskFlow: CRUD, base de datos y middleware."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # Registra las tablas en Base.metadata.
from app.database import Base, engine
from app.errors import unhandled_exception_handler
from app.middleware import ProcessTimeMiddleware
from app.routers import categories, projects, status, tasks, users


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Crea las tablas que falten y libera conexiones al terminar."""
    try:
        Base.metadata.create_all(bind=engine)
        yield
    finally:
        engine.dispose()


tags_metadata = [
    {
        "name": "tasks",
        "description": (
            "CRUD de tareas con filtros, ordenación y paginación."
        ),
    },
    {
        "name": "projects",
        "description": (
            "CRUD de proyectos, tareas asociadas y contadores."
        ),
    },
    {
        "name": "categories",
        "description": (
            "CRUD de categorías, tareas asociadas y contadores."
        ),
    },
    {
        "name": "users",
        "description": (
            "Usuarios de prueba y dependencias anidadas. "
            "X-User-ID no constituye autenticación."
        ),
    },
    {
        "name": "status",
        "description": "Salud, versión y conectividad.",
    },
]


api = FastAPI(
    title="TaskFlow API",
    description=(
        "Práctica 1.6: CRUD completo de tareas, proyectos y categorías "
        "con SQLAlchemy y SQLite."
    ),
    version="1.0.0",
    debug=False,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# Manejo global de excepciones no controladas.
api.add_exception_handler(Exception, unhandled_exception_handler)

# Rutas de la aplicación.
api.include_router(tasks.router)
api.include_router(projects.router)
api.include_router(categories.router)
api.include_router(users.router)
api.include_router(status.router)

# Rutas de depuración opcionales.
if os.getenv("ENABLE_DEBUG_ROUTES", "false").lower() == "true":
    from app.routers import debug

    api.include_router(debug.router)

# Orígenes permitidos para las peticiones desde el navegador.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]

if "*" in allowed_origins:
    raise ValueError("CORS_ORIGINS debe contener orígenes explícitos.")

# CORS incluye los métodos utilizados por el CRUD.
cors_app = CORSMiddleware(
    app=api,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "X-User-ID"],
    expose_headers=["X-Process-Time", "X-Request-ID"],
)

# Tiempo de procesamiento y trazabilidad de las peticiones.
app = ProcessTimeMiddleware(cors_app)