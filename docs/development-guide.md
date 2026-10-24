# Guía de Desarrollo: Cómo Implementar un Nuevo Recurso

Esta guía describe el flujo de trabajo estándar paso a paso para crear una nueva entidad completa en el proyecto. 

Para este tutorial, crearemos el recurso **`User`** (`/users`), cubriendo desde el esquema de datos hasta las pruebas automatizadas.

---

## 🧭 Flujo de Trabajo (Orden de Implementación)

0. **[Paso 0: Crear la rama del feature en Git](#paso-0-crear-la-rama-del-feature-en-git)** (`feat/FEAT-XXX-slug`)
1. **[Paso 1: Schemas y DTOs](#paso-1-definir-schemas-y-dtos)** (`src/app/schemas/user.py`)
2. **[Paso 2: Protocolo de Persistencia](#paso-2-definir-el-protocolo-de-persistencia)** (`src/app/repositories/base.py`)
3. **[Paso 3: Repositorio Turso](#paso-3-implementar-el-repositorio)** (`src/app/repositories/user_repository.py`)
4. **[Paso 4: Servicio de Negocio](#paso-4-implementar-el-servicio-de-negocio)** (`src/app/services/user_service.py`)
5. **[Paso 5: Controlador y Rutas](#paso-5-crear-el-controlador-y-rutas-http)** (`src/app/api/routes/users.py`)
6. **[Paso 6: Registro en el Entrypoint](#paso-6-registrar-las-rutas-en-mainpy)** (`src/app/main.py`)
7. **[Paso 7: Pruebas Automatizadas](#paso-7-escribir-pruebas-unitarias-e-integrales)** (`tests/`)

---

## Paso 0: Crear la rama del feature en Git

Antes de escribir cualquier línea de código, sitúate en `main` actualizado y crea una nueva rama de corta duración con el identificador del requerimiento:

```bash
git checkout main
git pull origin main
git checkout -b feat/FEAT-001-usuarios-crud
```

> [!IMPORTANT]
> Nunca implementes código directamente sobre la rama `main`. Toda modificación debe vivir en su rama temática y reintegrarse a `main` tras superar la suite de pruebas.

---

## Paso 1: Definir Schemas y DTOs

Crea el archivo `src/app/schemas/user.py` con los modelos de Pydantic v2:

```python
# src/app/schemas/user.py
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico único del usuario")
    full_name: str = Field(..., min_length=2, max_length=120, description="Nombre completo")
    is_active: bool = Field(default=True, description="Estado del usuario")


class UserCreateRequest(UserBase):
    """Payload recibido en POST /users."""


class UserUpdateRequest(BaseModel):
    """Payload recibido en PUT /users/<user_id>."""
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    is_active: bool | None = Field(default=None)


class UserResponse(UserBase):
    """DTO devuelto por la API."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Identificador único (UUID)")
    created_at: str | None = Field(default=None, description="Fecha de creación ISO-8601")


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
```

---

## Paso 2: Definir el Protocolo de Persistencia

Agrega la interfaz en `src/app/repositories/base.py` para desacoplar el servicio del repositorio:

```python
# En src/app/repositories/base.py
from app.schemas.user import UserResponse


class UserRepositoryProtocol(Protocol):
    def init_table(self) -> None: ...
    def save(self, user_id: str, email: str, full_name: str, is_active: bool, created_at: str | None = None) -> UserResponse: ...
    def find_by_id(self, user_id: str) -> UserResponse | None: ...
    def find_by_email(self, email: str) -> UserResponse | None: ...
    def find_all(self, limit: int = 50, offset: int = 0) -> list[UserResponse]: ...
    def delete(self, user_id: str) -> bool: ...
```

---

## Paso 3: Implementar el Repositorio

Crea `src/app/repositories/user_repository.py` con las consultas SQL a Turso:

```python
# src/app/repositories/user_repository.py
from datetime import datetime, timezone
from typing import Callable
from aws_lambda_powertools import Logger

from app.core.database import get_turso_connection
from app.schemas.user import UserResponse

logger = Logger(child=True)


class UserRepository:
    def __init__(self, connection_factory: Callable | None = None):
        self._get_connection = connection_factory or get_turso_connection

    def init_table(self) -> None:
        conn = self._get_connection()
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            is_active INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

    def save(
        self,
        user_id: str,
        email: str,
        full_name: str,
        is_active: bool,
        created_at: str | None = None,
    ) -> UserResponse:
        if not created_at:
            created_at = datetime.now(timezone.utc).isoformat()

        conn = self._get_connection()
        query = """
        INSERT INTO users (id, email, full_name, is_active, created_at)
        VALUES (?, ?, ?, ?, ?);
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id, email, full_name, int(is_active), created_at))
            conn.commit()

        return UserResponse(
            id=user_id,
            email=email,
            full_name=full_name,
            is_active=is_active,
            created_at=created_at,
        )

    def find_by_id(self, user_id: str) -> UserResponse | None:
        conn = self._get_connection()
        query = "SELECT id, email, full_name, is_active, created_at FROM users WHERE id = ?;"
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return UserResponse(
                id=row[0],
                email=row[1],
                full_name=row[2],
                is_active=bool(row[3]),
                created_at=row[4],
            )

    def find_by_email(self, email: str) -> UserResponse | None:
        conn = self._get_connection()
        query = "SELECT id, email, full_name, is_active, created_at FROM users WHERE email = ?;"
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if not row:
                return None
            return UserResponse(
                id=row[0],
                email=row[1],
                full_name=row[2],
                is_active=bool(row[3]),
                created_at=row[4],
            )
```

---

## Paso 4: Implementar el Servicio de Negocio

Crea `src/app/services/user_service.py` con las reglas de dominio:

```python
# src/app/services/user_service.py
import uuid
from aws_lambda_powertools import Logger

from app.core.exceptions import AppException, ItemNotFoundError
from app.repositories.base import UserRepositoryProtocol
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreateRequest, UserListResponse, UserResponse

logger = Logger(child=True)


class UserAlreadyExistsError(AppException):
    """Lanzada cuando el email ya está registrado."""


class UserService:
    def __init__(self, repository: UserRepositoryProtocol | None = None):
        self.repository = repository or UserRepository()

    def create_user(self, dto: UserCreateRequest) -> UserResponse:
        # Regla de negocio: Verificar unicidad del email
        existing = self.repository.find_by_email(dto.email)
        if existing:
            raise UserAlreadyExistsError(f"El email '{dto.email}' ya está registrado.")

        user_id = str(uuid.uuid4())
        return self.repository.save(
            user_id=user_id,
            email=dto.email.lower().strip(),
            full_name=dto.full_name.strip(),
            is_active=dto.is_active,
        )

    def get_user(self, user_id: str) -> UserResponse:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ItemNotFoundError(f"Usuario con id '{user_id}' no encontrado.")
        return user
```

---

## Paso 5: Crear el Controlador y Rutas HTTP

Crea `src/app/api/routes/users.py`:

```python
# src/app/api/routes/users.py
from aws_lambda_powertools.event_handler.api_gateway import Response
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError
from pydantic import ValidationError

from app.api.router import router
from app.core.exceptions import ItemNotFoundError
from app.schemas.user import UserCreateRequest
from app.services.user_service import UserAlreadyExistsError, UserService

user_service = UserService()


@router.post("/users")
def create_user():
    raw_body = router.current_event.json_body
    if not raw_body:
        raise BadRequestError("Cuerpo de solicitud requerido.")

    try:
        dto = UserCreateRequest(**raw_body)
    except ValidationError as exc:
        raise BadRequestError(str(exc))

    try:
        created = user_service.create_user(dto)
        return Response(
            status_code=201,
            content_type="application/json",
            body=created.model_dump_json(),
        )
    except UserAlreadyExistsError as exc:
        raise BadRequestError(str(exc))


@router.get("/users/<user_id>")
def get_user(user_id: str) -> dict:
    try:
        user = user_service.get_user(user_id)
        return user.model_dump()
    except ItemNotFoundError as exc:
        raise NotFoundError(str(exc))
```

---

## Paso 6: Registrar las Rutas en `main.py`

Agrega el import en `src/app/main.py` para que Powertools indexe las rutas:

```python
# En src/app/main.py
import app.api.routes.health  # noqa: F401
import app.api.routes.items  # noqa: F401
import app.api.routes.users  # noqa: F401  <-- NUEVA LÍNEA
```

---

## Paso 7: Escribir Pruebas Automatizadas

1. **Prueba unitaria del servicio** en `tests/unit/test_user_service.py`:
   - Mockea `UserRepository`.
   - Verifica que lance `UserAlreadyExistsError` si el email ya existe.
   - Verifica que retorne `UserResponse` con el UUID generado.

2. **Ejecutar la suite completa:**
   ```bash
   uv run pytest -v
   uv run ruff check .
   ```
