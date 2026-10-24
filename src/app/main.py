"""Punto de entrada principal (Handler) para AWS Lambda."""

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

# Registro explícito de rutas para que el router de Powertools las indexe
import app.api.routes.health
import app.api.routes.items  # noqa: F401
from app.api.router import router

logger = Logger(service="turso-api-service")


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """Manejador principal de eventos HTTP invocados desde API Gateway HTTP API v2."""
    return router.resolve(event, context)
