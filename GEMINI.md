# Reglas y Directrices de Desarrollo (Antigravity Guide)

Bienvenido al repositorio **python_lambda_template**. Este documento y las directrices en `.agents/rules/` definen la forma estándar de trabajar en el proyecto para garantizar la consistencia técnica, el desacoplamiento de capas y la calidad del código a lo largo del tiempo.

---

## 🎯 Misión del Proyecto

Construir APIs serverless en **AWS Lambda** (Python 3.13) expuestas mediante **API Gateway HTTP API (Payload Format 2.0)** y conectadas a la base de datos distribuida serverless **Turso (libSQL)**, aplicando **Clean Architecture** para separar estrictamente el enrutamiento HTTP, la validación de contratos, la lógica de negocio y la persistencia.

---

## 🧭 Pilares Técnicos y Arquitectónicos

1. **Clean Architecture / Separación de Responsabilidades:**
   - La capa de transporte HTTP (`src/app/api/`) procesa eventos de API Gateway y valida contratos con Pydantic. Nunca contiene reglas de negocio ni ejecuta consultas SQL.
   - La capa de lógica de negocio (`src/app/services/`) orquesta las reglas de dominio. Desconoce conceptos HTTP (`request`, `response`, `statusCode`) y la tecnología de base de datos.
   - La capa de persistencia (`src/app/repositories/`) implementa interfaces abstractas (`Protocol`) y ejecuta SQL parametrizado sobre Turso.
   - La capa transversal (`src/app/core/`) gestiona la conexión singleton a Turso y la resolución de secretos (AWS Secrets Manager en prod, `.env` en local).

2. **Acceso a Datos Serverless con Turso:**
   - Utilizar el driver DB-API 2.0 `turso-serverless` sobre HTTPS (100% Pure Python, sin binarios C/Rust).
   - Consultas siempre parametrizadas mediante el marcador `?` para prevenir inyecciones SQL.
   - Reutilización de conexión a nivel de módulo para optimizar *warm starts*.

3. **Tipado Moderno en Python 3.13:**
   - Aprovechar las capacidades nativas de Python 3.13 (`X | None` en vez de `Optional[X]`, `list[T]` en vez de `List[T]`).
   - Todos los contratos de entrada y salida deben tiparse mediante Pydantic v2.

4. **Calidad y Verificación Continua:**
   - Antes de considerar completada cualquier tarea o refactorización:
     - `uv run pytest -v` debe pasar con 100% de éxito.
     - `uv run ruff check .` no debe arrojar advertencias ni errores.

5. **Flujo de Trabajo y Backlog:**
   - Toda nueva funcionalidad debe contar con una especificación en `backlog/pending/` siguiendo `backlog/TEMPLATE.md`.
   - **Creación obligatoria de rama previa:** Antes de modificar o crear código para cualquier requerimiento del backlog, se debe crear una rama de corta duración basada en `main` siguiendo la convención (`git checkout -b feat/FEAT-XXX-slug main`). Nunca implementar directamente en `main`.
   - Adherirse a **Trunk-Based Development** con merges frecuentes a `main` y **Conventional Commits** (`feat:`, `fix:`, etc.).
   - Al finalizar, mover el requerimiento a `backlog/completed/` y actualizar `CHANGELOG.md`.

---

## 📚 Enlaces a Reglas Detalladas

Para directrices especializadas por ámbito, consulta:

- 🏛️ **[Reglas de Arquitectura](.agents/rules/architecture.md)**: Flujo de dependencias, estructura de capas y DTOs.
- ⚡ **[Reglas de Base de Datos y Turso](.agents/rules/database.md)**: Conexión sobre HTTPS, warm starts, DDL y consultas parametrizadas.
- 🧪 **[Reglas de Calidad y Testing](.agents/rules/quality.md)**: Estándares de testing unitario e integración, linters y tipado.
- 🌳 **[Reglas de Workflow y Backlog](.agents/rules/workflow.md)**: Trunk-Based Development, Conventional Commits y ciclo de vida del backlog.
