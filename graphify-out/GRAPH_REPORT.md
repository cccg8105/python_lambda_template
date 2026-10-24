# Graph Report - python_lambda_template  (2026-10-23)

## Corpus Check
- Corpus is ~9,694 words - fits in a single context window. You may not need a graph.

## Summary
- 208 nodes · 338 edges · 27 communities (9 shown, 18 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 54 edges (avg confidence: 0.91)
- Token cost: 1,250 input · 850 output

## Community Hubs (Navigation)
- Schemas, DTOs & Item Service
- Item Repository & Turso DDL
- Lambda Handler, Router & Turso DB
- Items HTTP API Route Controllers
- Core Config & Secrets Manager
- Domain Exceptions Hierarchy
- Service Unit Testing Suite
- API Gateway Integration Tests
- Test Fixtures & Mock Context
- Architecture & System Design Docs
- Turso & Persistence Guides
- AWS SAM Template Infrastructure
- Project Readme & Overview
- Clean Architecture Concepts
- Warm Start Connection Re-use
- Pure Python Turso DB-API
- Documentation Index & Navigation

## God Nodes (most connected - your core abstractions)
1. `ItemResponse` - 25 edges
2. `ItemRepository` - 21 edges
3. `ItemService` - 17 edges
4. `ItemNotFoundError` - 16 edges
5. `ItemRepositoryProtocol` - 13 edges
6. `ItemUpdateRequest` - 10 edges
7. `ItemCreateRequest` - 9 edges
8. `lambda_handler()` - 8 edges
9. `get_turso_credentials()` - 7 edges
10. `AppException` - 7 edges

## Surprising Connections (you probably didn't know these)
- `test_get_item_not_found_returns_404()` --uses--> `ItemNotFoundError`  [INFERRED]
  tests/integration/test_routes.py → src/app/core/exceptions.py
- `test_create_item_valid_payload()` --uses--> `ItemResponse`  [INFERRED]
  tests/integration/test_routes.py → src/app/schemas/item.py
- `test_get_item_found()` --uses--> `ItemResponse`  [INFERRED]
  tests/unit/test_services.py → src/app/schemas/item.py
- `test_update_item_success()` --uses--> `ItemResponse`  [INFERRED]
  tests/unit/test_services.py → src/app/schemas/item.py
- `item_service()` --uses--> `ItemService`  [INFERRED]
  tests/unit/test_services.py → src/app/services/item_service.py

## Import Cycles
- None detected.

## Communities (27 total, 18 thin omitted)

### Community 0 - "Schemas, DTOs & Item Service"
Cohesion: 0.08
Nodes (8): ItemRepositoryProtocol, ItemBase, ItemCreateRequest, ItemListResponse, ItemResponse, ItemService, test_create_item_success(), test_list_items()

### Community 1 - "Item Repository & Turso DDL"
Cohesion: 0.13
Nodes (9): initialize_database(), ItemRepository, create_mock_connection(), test_delete_returns_true_when_found(), test_find_all_returns_list(), test_find_by_id_returns_item_when_exists(), test_find_by_id_returns_none_when_not_found(), test_init_table_executes_ddl() (+1 more)

### Community 2 - "Lambda Handler, Router & Turso DB"
Cohesion: 0.10
Nodes (4): health_check(), get_turso_connection(), reset_turso_connection(), set_turso_connection()

### Community 3 - "Items HTTP API Route Controllers"
Cohesion: 0.13
Nodes (10): ItemNotFoundError, ItemUpdateRequest, item_service(), mock_repository(), test_delete_item_not_found_raises_exception(), test_delete_item_success(), test_get_item_found(), test_get_item_not_found_raises_exception() (+2 more)

### Community 4 - "Core Config & Secrets Manager"
Cohesion: 0.12
Nodes (5): create_item(), delete_item(), get_item(), list_items(), update_item()

### Community 5 - "Domain Exceptions Hierarchy"
Cohesion: 0.17
Nodes (4): get_turso_credentials(), AppException, DatabaseConnectionError, ItemAlreadyExistsError

### Community 6 - "Service Unit Testing Suite"
Cohesion: 0.28
Nodes (6): lambda_handler(), build_apigw_v2_event(), test_create_item_invalid_payload_returns_400(), test_create_item_valid_payload(), test_get_item_not_found_returns_404(), test_health_check_route()

### Community 7 - "API Gateway Integration Tests"
Cohesion: 0.24
Nodes (3): lambda_context(), LambdaContextMock, setup_test_environment()

### Community 8 - "Test Fixtures & Mock Context"
Cohesion: 0.50
Nodes (3): Completed Features History, Clean Architecture & Design, FEAT-000: Plantilla Base Serverless

## Knowledge Gaps
- **9 isolated node(s):** `python-lambda-turso-template`, `New Resource Development Guide`, `API Conventions & HTTP API v2`, `Automated Testing Strategy`, `Trunk-Based Development & SemVer` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 111 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ItemResponse` connect `Schemas, DTOs & Item Service` to `Item Repository & Turso DDL`, `Lambda Handler, Router & Turso DB`, `Items HTTP API Route Controllers`, `Service Unit Testing Suite`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `ItemResponse` (e.g. with `ItemRepositoryProtocol` and `ItemRepository`) actually correct?**
  _`ItemResponse` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `python-lambda-turso-template`, `New Resource Development Guide`, `API Conventions & HTTP API v2` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Schemas, DTOs & Item Service` be split into smaller, more focused modules?**
  _Cohesion score 0.08461538461538462 - nodes in this community are weakly interconnected._
- **Why does `ItemRepository` connect `Item Repository & Turso DDL` to `Schemas, DTOs & Item Service`, `Lambda Handler, Router & Turso DB`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `ItemRepository` (e.g. with `initialize_database()` and `ItemResponse`) actually correct?**
  _`ItemRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `Item Repository & Turso DDL` be split into smaller, more focused modules?**
  _Cohesion score 0.13105413105413105 - nodes in this community are weakly interconnected._