"""Manejo de excepciones no controladas sin exponer detalles al cliente."""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


logger = logging.getLogger("uvicorn.error")


class ErrorResponse(BaseModel):
    """Formato de respuesta para errores internos."""

    error: str
    error_code: str
    request_id: str


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Registra el error completo y devuelve un mensaje público genérico."""

    request_id = getattr(request.state, "request_id", "unknown")

    # El detalle técnico queda en los registros del servidor.
    logger.error(
        "Excepción no controlada: request_id=%s method=%s path=%s",
        request_id,
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )

    # El cliente recibe información útil sin el traceback ni str(exc).
    error_response = ErrorResponse(
        error="Se ha producido un error interno en el servidor.",
        error_code="INTERNAL_SERVER_ERROR",
        request_id=request_id,
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(),
    )