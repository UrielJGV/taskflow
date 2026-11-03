"""Configuración de TaskFlow, routers y middleware."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.errors import unhandled_exception_handler
from app.middleware import ProcessTimeMiddleware
from app.routers import projects, status, tasks


tags_metadata = [
    {
        "name": "tasks",
        "description": "Operaciones simuladas de tareas.",
    },
    {
        "name": "projects",
        "description": "Operaciones simuladas de proyectos.",
    },
    {
        "name": "status",
        "description": "Salud, versión y conectividad.",
    },
]


api = FastAPI(
    title="TaskFlow API",
    description="API con routers, CORS, trazabilidad y manejo de errores.",
    version="1.0.0",
    debug=False,
    openapi_tags=tags_metadata,
)

# Registra el handler global de excepciones no controladas.
api.add_exception_handler(Exception, unhandled_exception_handler)

# Conserva las rutas de las prácticas anteriores.
api.include_router(tasks.router)
api.include_router(projects.router)
api.include_router(status.router)

# La ruta de error solo se registra cuando se habilita expresamente.
if os.getenv("ENABLE_DEBUG_ROUTES", "false").lower() == "true":
    from app.routers import debug

    api.include_router(debug.router)

# Permite configurar una lista de orígenes mediante el entorno.
# Si no se configura, utiliza el frontend local de la práctica.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]

# Evita permitir indiscriminadamente cualquier origen.
if "*" in allowed_origins:
    raise ValueError("CORS_ORIGINS debe contener orígenes explícitos.")

# Envuelve la aplicación completa para incluir CORS también en los 500.
cors_app = CORSMiddleware(
    app=api,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
    expose_headers=["X-Process-Time", "X-Request-ID"],
)

# Capa externa: añade cabeceras incluso a errores y preflight de CORS.
app = ProcessTimeMiddleware(cors_app)