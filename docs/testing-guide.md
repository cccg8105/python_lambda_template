# Guía de Pruebas (Testing Guide)

Este documento describe la estrategia de pruebas automatizadas del proyecto, cómo estructurar nuevos tests y cómo ejecutarlos de forma eficiente con `uv` y `pytest`.

---

## 🎯 Pirámide de Pruebas en el Proyecto

```text
       /\
      /  \     Pruebas de Integración (API Gateway v2 Events)
     /----\    tests/integration/test_routes.py
    /      \
   /--------\  Pruebas Unitarias (Lógica de Negocio y Repositorios)
  /          \ tests/unit/test_services.py, tests/unit/test_repositories.py
 /------------\
```

1. **Pruebas Unitarias de Servicios (`tests/unit/test_services.py`):**
   - Evalúan la lógica de negocio pura.
   - El repositorio se sustituye por un `MagicMock`.
   - **No realizan conexiones a base de datos ni llamadas de red.** Son instantáneas.

2. **Pruebas Unitarias de Repositorios (`tests/unit/test_repositories.py`):**
   - Evalúan que las consultas SQL parametrizadas (`?`) se construyan correctamente y se invoque `conn.commit()`.
   - Utilizan mocks del protocolo DB-API 2.0 (`cursor`, `execute`, `fetchone`, `fetchall`).

3. **Pruebas de Integración de Rutas (`tests/integration/test_routes.py`):**
   - Validan el flujo completo desde el `lambda_handler`.
   - Utilizan la función auxiliar `build_apigw_v2_event(...)` para generar un evento fiel a API Gateway HTTP API v2.
   - Verifican la serialización de respuestas (`statusCode`, `body` JSON, cabeceras).

---

## ⚙️ Configuración del Entorno de Pruebas (`tests/conftest.py`)

Para garantizar que las pruebas nunca intenten comunicarse con AWS real o con Turso durante los tests:

```python
# tests/conftest.py
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    monkeypatch.setenv("AWS_SAM_LOCAL", "true")
    monkeypatch.setenv("TURSO_DATABASE_URL", "libsql://test-db.turso.io")
    monkeypatch.setenv("TURSO_AUTH_TOKEN", "mock-turso-token")
    monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-turso-service")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
```

El fixture `lambda_context` provee un contexto simulado de AWS Lambda con `function_name`, `memory_limit_in_mb` y `aws_request_id`.

---

## 🧪 Cómo Escribir Pruebas para un Nuevo Servicio

Al agregar un nuevo servicio (ej. `UserService`), escribe su prueba unitaria así:

```python
# tests/unit/test_user_service.py
from unittest.mock import MagicMock
import pytest
from app.services.user_service import UserService, UserAlreadyExistsError
from app.schemas.user import UserCreateRequest, UserResponse

def test_create_user_success():
    # 1. Arrange (Preparar)
    mock_repo = MagicMock()
    mock_repo.find_by_email.return_value = None
    mock_repo.save.return_value = UserResponse(
        id="usr-123", email="ana@example.com", full_name="Ana Pérez", is_active=True
    )
    service = UserService(repository=mock_repo)

    # 2. Act (Ejecutar)
    req = UserCreateRequest(email="ana@example.com", full_name="Ana Pérez")
    result = service.create_user(req)

    # 3. Assert (Verificar)
    assert result.id == "usr-123"
    assert result.email == "ana@example.com"
    mock_repo.save.assert_called_once()

def test_create_user_duplicate_email_raises_error():
    mock_repo = MagicMock()
    # Simula que el usuario ya existe
    mock_repo.find_by_email.return_value = UserResponse(
        id="usr-1", email="ana@example.com", full_name="Ana", is_active=True
    )
    service = UserService(repository=mock_repo)

    req = UserCreateRequest(email="ana@example.com", full_name="Ana")
    with pytest.raises(UserAlreadyExistsError):
        service.create_user(req)
```

---

## 🚀 Comandos de Ejecución

### Ejecutar todas las pruebas:
```bash
uv run pytest -v
```

### Ejecutar un archivo específico:
```bash
uv run pytest tests/unit/test_services.py -v
```

### Ejecutar una prueba por nombre (filtro `-k`):
```bash
uv run pytest -k "test_create_item" -v
```

### Verificar estilo y formato del código:
```bash
uv run ruff check .
uv run ruff format .
```
