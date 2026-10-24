# FEAT-001: Módulo de Gestión de Usuarios (CRUD)

| Metadato | Valor |
| :--- | :--- |
| **ID** | `FEAT-001` |
| **Tipo** | Feature |
| **Versión Objetivo** | `v0.2.0` |
| **Estado** | `Pendiente` |
| **Autor** | Equipo de Desarrollo |
| **Fecha de Creación** | 2026-10-23 |
| **Fecha de Finalización** | - |

---

## 1. Historia de Usuario

> **Como** consumidor de la API  
> **Quiero** poder registrar, consultar y administrar usuarios con validación de correo único  
> **Para** habilitar la gestión de perfiles de usuario en la plataforma.

### Contexto / Problema:
Actualmente la API solo dispone de la gestión de `Items`. Se requiere incorporar el recurso `Users` (`/users`) como parte de la versión `v0.2.0`, garantizando que no se puedan duplicar correos electrónicos y aplicando la arquitectura en capas desacoplada.

---

## 2. Criterios de Aceptación (Acceptance Criteria)

- [ ] **Escenario 1 - Registro Exitoso (`POST /users`):**
  - *Dado que* se envía un JSON con `email` válido y no existente, y `full_name`.
  - *Cuando* se invoque `POST /users`.
  - *Entonces* debe responder HTTP `201 Created` con el objeto del usuario creado (incluyendo `id` UUID generado y `created_at` ISO-8601).

- [ ] **Escenario 2 - Email Duplicado (`POST /users`):**
  - *Dado que* el email ya se encuentra registrado en Turso.
  - *Cuando* se invoque `POST /users` con ese mismo email.
  - *Entonces* debe responder HTTP `400 Bad Request` indicando que el correo ya está en uso.

- [ ] **Escenario 3 - Consulta por ID (`GET /users/<user_id>`):**
  - *Dado que* existe un usuario con dicho `user_id`.
  - *Cuando* se invoque `GET /users/<user_id>`.
  - *Entonces* debe responder HTTP `200 OK` con los datos del usuario.

- [ ] **Escenario 4 - Usuario Inexistente (`GET /users/<user_id>`):**
  - *Dado que* no existe un usuario con dicho `user_id`.
  - *Cuando* se invoque `GET /users/<user_id>`.
  - *Entonces* debe responder HTTP `404 Not Found`.

---

## 3. Desglose de Tareas Técnicas por Capa

- [ ] **Contratos / DTOs (`src/app/schemas/user.py`):**
  - `UserCreateRequest` (`email: EmailStr`, `full_name: str`, `is_active: bool = True`).
  - `UserUpdateRequest` (`full_name: str | None`, `is_active: bool | None`).
  - `UserResponse` (`id: str`, `email: str`, `full_name: str`, `is_active: bool`, `created_at: str`).
  - `UserListResponse` (`users: list[UserResponse]`, `total: int`).

- [ ] **Persistencia (`src/app/repositories/`):**
  - Agregar `UserRepositoryProtocol` en `base.py`.
  - Crear `UserRepository` en `user_repository.py` con DDL `CREATE TABLE IF NOT EXISTS users (...)` y consultas SQL parametrizadas (`save`, `find_by_id`, `find_by_email`, `find_all`, `delete`).

- [ ] **Lógica de Negocio (`src/app/services/user_service.py`):**
  - Crear `UserService` con validación de unicidad de email antes de persistir.
  - Lanzar `UserAlreadyExistsError` si el correo está ocupado.
  - Lanzar `ItemNotFoundError` si el ID no existe en consultas o eliminaciones.

- [ ] **Enrutamiento HTTP (`src/app/api/routes/users.py`):**
  - Endpoints `POST /users`, `GET /users`, `GET /users/<user_id>`, `DELETE /users/<user_id>`.
  - Mapeo de excepciones de dominio a HTTP `400` y `404`.
  - Registrar ruta en `src/app/main.py`.

- [ ] **Pruebas Automatizadas (`tests/`):**
  - `tests/unit/test_user_service.py`: Pruebas de reglas de negocio con mock de repositorio.
  - `tests/unit/test_user_repository.py`: Pruebas de SQL con mock de DB-API.
  - `tests/integration/test_user_routes.py`: Integración con eventos simulados de API Gateway v2.

---

## 4. Definition of Done (DoD) - Checklist de Finalización

- [ ] Todos los criterios de aceptación probados y funcionando.
- [ ] `uv run pytest -v` con 100% de éxito.
- [ ] `uv run ruff check .` limpio.
- [ ] Mover este archivo a `backlog/completed/FEAT-001-usuarios-crud.md`.
- [ ] Actualizar [backlog/pending/README.md](README.md) y [backlog/completed/README.md](../completed/README.md).
- [ ] Registrar en [CHANGELOG.md](../../CHANGELOG.md) bajo la versión `[0.2.0]`.
- [ ] Merge a `main` con commit: `feat(users): implementar modulo de gestion de usuarios CRUD`.
- [ ] Git tag `v0.2.0`.
