"""Módulo transversal de logging estructurado y trazabilidad con AWS Lambda Powertools."""

from __future__ import annotations

import functools
import inspect
import logging
import os
import time
from collections.abc import Callable
from typing import Any

from aws_lambda_powertools import Logger
from pydantic import BaseModel

# Inicialización del Logger central de Powertools respetando LOG_LEVEL y POWERTOOLS_SERVICE_NAME
logger = Logger(
    service=os.getenv("POWERTOOLS_SERVICE_NAME", "turso-api-service"),
    level=os.getenv("LOG_LEVEL", "INFO"),
)

SENSITIVE_KEYWORDS = {
    "password",
    "token",
    "secret",
    "auth",
    "key",
    "credential",
    "api_key",
    "access_key",
    "authorization",
    "private",
}


def sanitize_data(data: Any, max_depth: int = 4) -> Any:
    """Enmascara recursivamente información sensible en diccionarios, modelos Pydantic o listas."""
    if max_depth <= 0:
        return "..."

    if data is None or isinstance(data, (bool, int, float)):
        return data

    if isinstance(data, BaseModel):
        data = data.model_dump()

    if isinstance(data, dict):
        sanitized_dict: dict[str, Any] = {}
        for key, value in data.items():
            key_str = str(key).lower()
            if any(sensitive in key_str for sensitive in SENSITIVE_KEYWORDS):
                sanitized_dict[key] = "[REDACTED]"
            else:
                sanitized_dict[key] = sanitize_data(value, max_depth - 1)
        return sanitized_dict

    if isinstance(data, (list, tuple, set)):
        return [sanitize_data(item, max_depth - 1) for item in data]

    # Para tipos no serializables nativamente
    return str(data) if not isinstance(data, str) else data


def _extract_bound_arguments(func: Callable, args: tuple, kwargs: dict) -> dict[str, Any]:
    """Extrae los argumentos de la función omitiendo 'self' y 'cls'."""
    try:
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        arguments = bound.arguments.copy()
        arguments.pop("self", None)
        arguments.pop("cls", None)
        return arguments
    except Exception:  # noqa: BLE001
        # Fallback en caso de funciones dinámicas
        return {"args": list(args), "kwargs": kwargs}


def trace_call(func: Callable) -> Callable:
    """Decorador transversal para trazabilidad de métodos.

    Registra entrada y salida a nivel INFO junto con inputs, outputs y duración (ms).
    Si el nivel de log es superior a INFO (ej. WARNING o ERROR), no incurre en sobrecarga.
    Si ocurre una excepción, la registra a nivel ERROR antes de re-lanzarla.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Optimización de rendimiento: Si el nivel no incluye INFO, omitir serialización
        if not logger.isEnabledFor(logging.INFO):
            return func(*args, **kwargs)

        func_name = f"{func.__module__}.{func.__qualname__}"
        bound_args = _extract_bound_arguments(func, args, kwargs)
        sanitized_inputs = sanitize_data(bound_args)

        logger.info(
            f"Invocando método: {func_name}",
            extra={"tracing": {"func": func_name, "inputs": sanitized_inputs}},
        )

        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            sanitized_output = sanitize_data(result)

            logger.info(
                f"Completado método: {func_name}",
                extra={
                    "tracing": {
                        "func": func_name,
                        "output": sanitized_output,
                        "duration_ms": duration_ms,
                    }
                },
            )
            return result
        except Exception:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.exception(
                f"Error en método: {func_name}",
                extra={"tracing": {"func": func_name, "duration_ms": duration_ms}},
            )
            raise

    return wrapper
