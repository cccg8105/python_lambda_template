# Comunidad 3: Items HTTP API Route Controllers

- **Cohesión interna:** 0.13
- **Cantidad de nodos:** 25

## 🧩 Miembros / Nodos

- **`pytest`** (pytest) - *Tipo:* `concept` | *Archivo:* ``
- **`src_app_core_exceptions_itemnotfounderror`** (ItemNotFoundError) - *Tipo:* `code` | *Archivo:* `src/app/core/exceptions.py`
- **`src_app_core_exceptions_rationale_13`** (Lanzada cuando un recurso no se encuentra en el repositorio.) - *Tipo:* `rationale` | *Archivo:* `src/app/core/exceptions.py`
- **`src_app_repositories_base_itemrepositoryprotocol_delete`** (.delete()) - *Tipo:* `code` | *Archivo:* `src/app/repositories/base.py`
- **`src_app_repositories_base_rationale_45`** (Elimina un item por su ID.) - *Tipo:* `rationale` | *Archivo:* `src/app/repositories/base.py`
- **`src_app_schemas_item_itemupdaterequest`** (ItemUpdateRequest) - *Tipo:* `code` | *Archivo:* `src/app/schemas/item.py`
- **`src_app_schemas_item_rationale_21`** (Payload para actualización parcial de un item.) - *Tipo:* `rationale` | *Archivo:* `src/app/schemas/item.py`
- **`src_app_services_item_service_itemservice_delete_item`** (.delete_item()) - *Tipo:* `code` | *Archivo:* `src/app/services/item_service.py`
- **`src_app_services_item_service_itemservice_get_item`** (.get_item()) - *Tipo:* `code` | *Archivo:* `src/app/services/item_service.py`
- **`src_app_services_item_service_itemservice_update_item`** (.update_item()) - *Tipo:* `code` | *Archivo:* `src/app/services/item_service.py`
- **`src_app_services_item_service_rationale_40`** (Obtiene un item por ID o eleva ItemNotFoundError.) - *Tipo:* `rationale` | *Archivo:* `src/app/services/item_service.py`
- **`src_app_services_item_service_rationale_52`** (Actualiza un item existente o eleva ItemNotFoundError.) - *Tipo:* `rationale` | *Archivo:* `src/app/services/item_service.py`
- **`src_app_services_item_service_rationale_67`** (Elimina un item por su ID o eleva ItemNotFoundError.) - *Tipo:* `rationale` | *Archivo:* `src/app/services/item_service.py`
- **`tests_unit_test_services`** (test_services.py) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_item_service`** (item_service()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_mock_repository`** (mock_repository()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_py_fixture`** (fixture) - *Tipo:* `code` | *Archivo:* ``
- **`tests_unit_test_services_rationale_1`** (Pruebas unitarias para la capa de servicios (lógica de negocio).) - *Tipo:* `rationale` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_test_delete_item_not_found_raises_exception`** (test_delete_item_not_found_raises_exception()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_test_delete_item_success`** (test_delete_item_success()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_test_get_item_found`** (test_get_item_found()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_test_get_item_not_found_raises_exception`** (test_get_item_not_found_raises_exception()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_test_update_item_not_found_raises_exception`** (test_update_item_not_found_raises_exception()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`tests_unit_test_services_test_update_item_success`** (test_update_item_success()) - *Tipo:* `code` | *Archivo:* `tests/unit/test_services.py`
- **`unittest_mock`** (unittest_mock) - *Tipo:* `concept` | *Archivo:* ``

---
[⬅️ Volver al Índice de la Wiki](index.md)