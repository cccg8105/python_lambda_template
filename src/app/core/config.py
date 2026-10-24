"""Gestión de configuración y credenciales para Turso."""

import json
import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities import parameters

from app.core.exceptions import DatabaseConnectionError

logger = Logger(child=True)


def get_turso_credentials() -> tuple[str, str]:
    """Obtiene la URL y el Token de autenticación de Turso.

    Prioridad:
    1. Variables de entorno locales (TURSO_DATABASE_URL, TURSO_AUTH_TOKEN)
       si se está ejecutando localmente (AWS_SAM_LOCAL o IS_LOCAL).
    2. AWS Secrets Manager con caché (max_age=300 segundos) vía Powertools Parameters.
    """
    is_local = (
        os.getenv("AWS_SAM_LOCAL", "").lower() in ("true", "1")
        or os.getenv("IS_LOCAL", "").lower() in ("true", "1")
        or bool(os.getenv("TURSO_DATABASE_URL"))
    )

    if is_local:
        db_url = os.getenv("TURSO_DATABASE_URL")
        auth_token = os.getenv("TURSO_AUTH_TOKEN", "")

        if not db_url:
            raise DatabaseConnectionError(
                "Variable de entorno TURSO_DATABASE_URL no configurada para entorno local."
            )
        return db_url, auth_token

    # Entorno AWS: recuperar de Secrets Manager con caché
    secret_name = os.getenv("TURSO_SECRET_NAME", "prod/turso/credentials")
    try:
        secret_raw = parameters.get_secret(secret_name, max_age=300)
        if not secret_raw:
            raise DatabaseConnectionError(f"Secreto vacío o inexistente: {secret_name}")

        secret_data = json.loads(secret_raw)
        db_url = secret_data.get("database_url") or secret_data.get("TURSO_DATABASE_URL")
        auth_token = secret_data.get("auth_token") or secret_data.get("TURSO_AUTH_TOKEN", "")

        if not db_url:
            raise DatabaseConnectionError(
                f"El secreto '{secret_name}' no contiene 'database_url' o 'TURSO_DATABASE_URL'."
            )
        return db_url, auth_token
    except Exception as exc:
        logger.error(f"Error al obtener credenciales desde Secrets Manager: {exc}")
        raise DatabaseConnectionError(f"Fallo al recuperar credenciales de Turso: {exc}") from exc
