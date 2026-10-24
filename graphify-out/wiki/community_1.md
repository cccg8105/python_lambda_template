# Comunidad 1: Item Repository & Turso DDL

- **Cohesión interna:** 0.13
- **Cantidad de nodos:** 27

## 🧩 Miembros / Nodos

- **`src_app_api_routes_health_initialize_database`** (initialize_database()) - *Tipo:* `code` | *Archivo:* `src/app/api/routes/health.py`
- **`src_app_api_routes_health_py_post`** (post) - *Tipo:* `code` | *Archivo:* ``
- **`src_app_api_routes_health_rationale_26`** (Endpoint de utilidad para crear las tablas necesarias en Turso si aún no…) - *Tipo:* `rationale` | *Archivo:* `src/app/api/routes/health.py`
- **`src_app_repositories_item_repository_itemrepository`** (ItemRepository) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_itemrepository_delete`** (.delete()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_itemrepository_find_all`** (.find_all()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_itemrepository_find_by_id`** (.find_by_id()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_itemrepository_init`** (.__init__()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_itemrepository_init_table`** (.init_table()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_itemrepository_save`** (.save()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_itemrepository_update`** (.update()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_114`** (Actualiza campos de un item existente.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_142`** (Elimina un item y devuelve True si fue eliminado.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_15`** (Repositorio de persistencia que ejecuta SQL parametrizado sobre Turso.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_21`** (Crea la tabla 'items' en Turso si aún no existe.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_45`** (Inserta un nuevo item en Turso y retorna su DTO.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_67`** (Obtiene un item por ID o None si no existe.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`src_app_repositories_item_repository_rationale_84`** (Retorna una lista de items ordenada por fecha descendente.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/item_repository.py`
- **`tests_unit_test_repositories`** (test_repositories.py) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_create_mock_connection`** (create_mock_connection()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_rationale_1`** (Pruebas unitarias para la capa de repositorios.) - *Tipo:* `rationale` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_test_delete_returns_true_when_found`** (test_delete_returns_true_when_found()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_test_find_all_returns_list`** (test_find_all_returns_list()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_test_find_by_id_returns_item_when_exists`** (test_find_by_id_returns_item_when_exists()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_test_find_by_id_returns_none_when_not_found`** (test_find_by_id_returns_none_when_not_found()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_test_init_table_executes_ddl`** (test_init_table_executes_ddl()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`
- **`tests_unit_test_repositories_test_save_inserts_and_commits`** (test_save_inserts_and_commits()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_repositories.py`

---
[⬅️ Volver al Índice de la Wiki](index.md)