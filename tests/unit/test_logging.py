"""Pruebas unitarias para el sistema de logging estructurado, sanitización y decorador @trace_call."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from app.core.logging import sanitize_data, trace_call


class SampleModel(BaseModel):
    username: str
    password: str
    api_token: str


def test_sanitize_data_masks_sensitive_keys():
    payload = {
        "user": "alice",
        "password": "supersecretpassword123",
        "auth_token": "bearer-xyz",
        "nested": {
            "api_key": "secret-key",
            "normal_field": "visible_value",
        },
    }

    sanitized = sanitize_data(payload)

    assert sanitized["user"] == "alice"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["auth_token"] == "[REDACTED]"
    assert sanitized["nested"]["api_key"] == "[REDACTED]"
    assert sanitized["nested"]["normal_field"] == "visible_value"


def test_sanitize_data_supports_pydantic_models():
    model = SampleModel(username="bob", password="my-password", api_token="tok-999")

    sanitized = sanitize_data(model)

    assert sanitized["username"] == "bob"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["api_token"] == "[REDACTED]"


def test_trace_call_logs_inputs_and_outputs_at_info():
    mock_logger = MagicMock()
    mock_logger.isEnabledFor.return_value = True

    with patch("app.core.logging.logger", mock_logger):

        @trace_call
        def calculate_sum(a: int, b: int) -> int:
            return a + b

        result = calculate_sum(5, 10)

        assert result == 15
        assert mock_logger.info.call_count == 2

        # Primera llamada: Entrada
        entry_call = mock_logger.info.call_args_list[0]
        assert "Invocando método:" in entry_call.args[0]
        assert entry_call.kwargs["extra"]["tracing"]["inputs"] == {"a": 5, "b": 10}

        # Segunda llamada: Salida
        exit_call = mock_logger.info.call_args_list[1]
        assert "Completado método:" in exit_call.args[0]
        assert exit_call.kwargs["extra"]["tracing"]["output"] == 15
        assert "duration_ms" in exit_call.kwargs["extra"]["tracing"]


def test_trace_call_skips_when_level_is_higher_than_info():
    mock_logger = MagicMock()
    mock_logger.isEnabledFor.return_value = False

    with patch("app.core.logging.logger", mock_logger):

        @trace_call
        def multiply(x: int, y: int) -> int:
            return x * y

        result = multiply(4, 5)

        assert result == 20
        assert mock_logger.info.call_count == 0


def test_trace_call_logs_exception_and_reraises():
    mock_logger = MagicMock()
    mock_logger.isEnabledFor.return_value = True

    with patch("app.core.logging.logger", mock_logger):

        @trace_call
        def faulty_operation():
            raise ValueError("Fallo catastrófico simulado")

        with pytest.raises(ValueError, match="Fallo catastrófico simulado"):
            faulty_operation()

        assert mock_logger.info.call_count == 1  # Entrada registrada
        assert mock_logger.exception.call_count == 1  # Error capturado

        error_call = mock_logger.exception.call_args_list[0]
        assert "Error en método:" in error_call.args[0]
        assert "duration_ms" in error_call.kwargs["extra"]["tracing"]
