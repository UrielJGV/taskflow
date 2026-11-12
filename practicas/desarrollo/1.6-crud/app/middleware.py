"""Middleware de tiempo de procesamiento y trazabilidad."""

import logging
from time import perf_counter
from uuid import uuid4

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


logger = logging.getLogger("uvicorn.error")


class ProcessTimeMiddleware:
    """Añade tiempo en milisegundos e identificador a cada respuesta HTTP."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        # Las conexiones no HTTP siguen su recorrido normal.
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        started_at = perf_counter()
        request_id = str(uuid4())

        # Permite consultar el identificador desde el handler de errores.
        scope.setdefault("state", {})["request_id"] = request_id

        async def send_with_headers(message: Message) -> None:
            # Añadimos las cabeceras justo antes de iniciar la respuesta.
            if message["type"] == "http.response.start":
                elapsed_ms = (perf_counter() - started_at) * 1000

                headers = MutableHeaders(scope=message)
                headers["X-Process-Time"] = f"{elapsed_ms:.3f}"
                headers["X-Request-ID"] = request_id

                logger.info(
                    "request_id=%s method=%s path=%s status=%s "
                    "process_time_ms=%.3f",
                    request_id,
                    scope["method"],
                    scope["path"],
                    message["status"],
                    elapsed_ms,
                )

            await send(message)

        await self.app(scope, receive, send_with_headers)