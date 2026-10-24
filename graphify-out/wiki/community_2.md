# Comunidad 2: Lambda Handler, Router & Turso DB

- **Cohesión interna:** 0.10
- **Cantidad de nodos:** 26

## 🧩 Miembros / Nodos

- **`any`** (Any) - *Tipo:* `code` | *Archivo:* ``
- **`aws_lambda_powertools`** (aws_lambda_powertools) - *Tipo:* `concept` | *Archivo:* ``
- **`aws_lambda_powertools_event_handler`** (aws_lambda_powertools_event_handler) - *Tipo:* `concept` | *Archivo:* ``
- **`aws_lambda_powertools_utilities_typing`** (aws_lambda_powertools_utilities_typing) - *Tipo:* `concept` | *Archivo:* ``
- **`collections_abc`** (collections_abc) - *Tipo:* `concept` | *Archivo:* ``
- **`datetime`** (datetime) - *Tipo:* `concept` | *Archivo:* ``
- **`src_app_api_router`** (router.py) - *Tipo:* `code` | *Archivo:* `src/app/api/router.py`
- **`src_app_api_router_rationale_1`** (Instancia principal del enrutador HTTP de Powertools para API Gateway v2.) - *Tipo:* `rationale` | *Archivo:* `src/app/api/router.py`
- **`src_app_api_routes_health`** (health.py) - *Tipo:* `code` | *Archivo:* `src/app/api/routes/health.py`
- **`src_app_api_routes_health_health_check`** (health_check()) - *Tipo:* `code` | *Archivo:* `src/app/api/routes/health.py`
- **`src_app_api_routes_health_py_get`** (get) - *Tipo:* `code` | *Archivo:* ``
- **`src_app_api_routes_health_rationale_1`** (Rutas para verificación de salud y utilidades del sistema.) - *Tipo:* `rationale` | *Archivo:* `src/app/api/routes/health.py`
- **`src_app_api_routes_health_rationale_16`** (Endpoint de comprobación de salud para monitoreo.) - *Tipo:* `rationale` | *Archivo:* `src/app/api/routes/health.py`
- **`src_app_core_database`** (database.py) - *Tipo:* `code` | *Archivo:* `src/app/core/database.py`
- **`src_app_core_database_get_turso_connection`** (get_turso_connection()) - *Tipo:* `code` | *Archivo:* `src/app/core/database.py`
- **`src_app_core_database_rationale_1`** (Gestión de conexión y ciclo de vida del cliente Turso Serverless.) - *Tipo:* `rationale` | *Archivo:* `src/app/core/database.py`
- **`src_app_core_database_rationale_16`** (Retorna una conexión activa a Turso Serverless (reutilizada en warm starts).…) - *Tipo:* `rationale` | *Archivo:* `src/app/core/database.py`
- **`src_app_core_database_rationale_33`** (Permite inyectar una conexión personalizada (útil para pruebas unitarias).) - *Tipo:* `rationale` | *Archivo:* `src/app/core/database.py`
- **`src_app_core_database_rationale_39`** (Cierra y reinicia la conexión global.) - *Tipo:* `rationale` | *Archivo:* `src/app/core/database.py`
- **`src_app_core_database_reset_turso_connection`** (reset_turso_connection()) - *Tipo:* `code` | *Archivo:* `src/app/core/database.py`
- **`src_app_core_database_set_turso_connection`** (set_turso_connection()) - *Tipo:* `code` | *Archivo:* `src/app/core/database.py`
- **`src_app_main`** (main.py) - *Tipo:* `code` | *Archivo:* `src/app/main.py`
- **`src_app_main_rationale_1`** (Punto de entrada principal (Handler) para AWS Lambda.) - *Tipo:* `rationale` | *Archivo:* `src/app/main.py`
- **`src_app_repositories_item_repository`** (item_repository.py) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_1`** (Implementación del repositorio de Items utilizando turso_serverless.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`turso_serverless`** (turso_serverless) - *Tipo:* `concept` | *Archivo:* ``

---
[⬅️ Volver al Índice de la Wiki](index.md)