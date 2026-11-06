"""Configuración de TaskFlow, base de datos, routers y middleware."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # Registra los modelos en Base.metadata.
from app.database import Base, engine
from app.errors import unhandled_exception_handler
from app.middleware import ProcessTimeMiddleware
from app.routers import projects, status, tasks, users


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Prepara las tablas al arrancar y libera conexiones al terminar."""
    try:
        Base.metadata.create_all(bind=engine)
        yield
    finally:
        engine.dispose()


tags_metadata = [
    {
        "name": "tasks",
        "description": "Creación y consulta de tareas guardadas en SQLite.",
    },
    {
        "name": "projects",
        "description": "Creación y consulta de proyectos guardados en SQLite.",
    },
    {
        "name": "users",
        "description": (
            "Usuarios de prueba y demostración de dependencias anidadas. "
            "La identificación mediante X-User-ID no es autenticación."
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
        "API con persistencia en SQLite mediante SQLAlchemy, "
        "inyección de dependencias, CORS, trazabilidad y manejo de errores."
    ),
    version="1.0.0",
    debug=False,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# Registra el manejador global de excepciones no controladas.
api.add_exception_handler(Exception, unhandled_exception_handler)

# Registra las rutas de la aplicación.
api.include_router(tasks.router)
api.include_router(projects.router)
api.include_router(users.router)
api.include_router(status.router)

# Activa las rutas de prueba solo cuando se solicita expresamente.
if os.getenv("ENABLE_DEBUG_ROUTES", "false").lower() == "true":
    from app.routers import debug

    api.include_router(debug.router)

# Lee los orígenes permitidos desde una variable de entorno.
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

# Incluye las cabeceras CORS también en las respuestas de error.
cors_app = CORSMiddleware(
    app=api,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-User-ID"],
    expose_headers=["X-Process-Time", "X-Request-ID"],
)

# Añade el tiempo de procesamiento y el identificador de petición.
app = ProcessTimeMiddleware(cors_app)