"""Rutas para comprobar el estado y la versión de TaskFlow."""

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Respuesta de la comprobación básica de salud."""

    status: str


router = APIRouter(tags=["status"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Comprobar el estado de la API",
    description="Comprueba que la aplicación responde correctamente.",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/version",
    summary="Consultar la versión de la API",
    description="Devuelve la versión actual de TaskFlow.",
)
def version() -> dict[str, str]:
    return {"version": "1.0.0"}


@router.get(
    "/ping",
    summary="Comprobar la conectividad",
    description="Devuelve una respuesta sencilla de comprobación.",
)
def ping() -> dict[str, str]:
    return {"message": "pong"}