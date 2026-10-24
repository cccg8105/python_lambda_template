"""Punto de entrada principal (Handler) para AWS Lambda."""

import uuid

from aws_lambda_powertools.utilities.typing import LambdaContext

# Registro explícito de rutas para que el router de Powertools las indexe
import app.api.routes.health
import app.api.routes.items  # noqa: F401
from app.api.router import router
from app.core.logging import logger


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """Manejador principal de eventos HTTP invocados desde API Gateway HTTP API v2."""
    correlation_id = str(uuid.uuid4())
    logger.set_correlation_id(correlation_id)

    response: dict = router.resolve(event, context)

    # Inyección de cabecera de correlación para el cliente
    headers = response.setdefault("headers", {})
    headers["X-Correlation-Id"] = correlation_id

    return response
