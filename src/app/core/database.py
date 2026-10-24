"""Gestión de conexión y ciclo de vida del cliente Turso Serverless."""

from typing import Any

import turso_serverless
from aws_lambda_powertools import Logger

from app.core.config import get_turso_credentials

logger = Logger(child=True)

_connection: Any | None = None


def get_turso_connection():
    """Retorna una conexión activa a Turso Serverless (reutilizada en warm starts).

    Utiliza el driver DB-API 2.0 de turso_serverless que envía consultas
    SQL sobre HTTPS, óptimo para entornos serverless y cold-starts rápidos.
    """
    global _connection
    if _connection is None:
        db_url, auth_token = get_turso_credentials()
        logger.info(f"Iniciando conexión a Turso: {db_url.split('@')[-1]}")
        _connection = turso_serverless.connect(
            url=db_url,
            auth_token=auth_token,
        )
    return _connection


def set_turso_connection(connection: Any) -> None:
    """Permite inyectar una conexión personalizada (útil para pruebas unitarias)."""
    global _connection
    _connection = connection


def reset_turso_connection() -> None:
    """Cierra y reinicia la conexión global."""
    global _connection
    if _connection is not None:
        try:
            _connection.close()
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"Detalle al cerrar conexión: {exc}")
        _connection = None
