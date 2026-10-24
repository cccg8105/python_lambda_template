"""Configuración y fixtures compartidas para pruebas."""

from dataclasses import dataclass

import pytest


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Establece variables de entorno seguras para pruebas unitarias."""
    monkeypatch.setenv("AWS_SAM_LOCAL", "true")
    monkeypatch.setenv("TURSO_DATABASE_URL", "libsql://test-db.turso.io")
    monkeypatch.setenv("TURSO_AUTH_TOKEN", "mock-turso-token")
    monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-turso-service")
    monkeypatch.setenv("POWERTOOLS_METRICS_NAMESPACE", "TestNamespace")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@dataclass
class LambdaContextMock:
    """Mock del contexto de ejecución de AWS Lambda."""

    function_name: str = "turso-api-function"
    memory_limit_in_mb: int = 256
    invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:turso-api"
    aws_request_id: str = "c6af9ac6-7b61-11e6-9a41-97e81422d07d"


@pytest.fixture
def lambda_context():
    """Fixture que provee un contexto mock de Lambda."""
    return LambdaContextMock()
