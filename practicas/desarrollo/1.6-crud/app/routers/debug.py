"""Ruta de diagnóstico para comprobar el manejador global de errores."""

from fastapi import APIRouter

from app.errors import ErrorResponse


router = APIRouter(prefix="/debug", tags=["debug"])


@router.get(
    "/error",
    summary="Provocar un error de prueba",
    description="Genera una excepción para comprobar la respuesta 500.",
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Error interno gestionado.",
        }
    },
)
def force_error():
    raise RuntimeError("Fallo de prueba: detalle interno del servidor.")