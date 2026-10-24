# Reglas de Arquitectura y Separación de Responsabilidades

Este documento detalla las directrices arquitectónicas que deben respetarse al agregar o modificar código en `src/app/`.

---

## 🏛️ Flujo Unidireccional de Capas

El flujo de información en la aplicación es estrictamente unidireccional:

$$\text{API Gateway v2} \longrightarrow \text{Router (Powertools)} \longrightarrow \text{Routes / Controllers} \longrightarrow \text{Services} \longrightarrow \text{Repositories} \longrightarrow \text{Turso DB}$$

### 1. Capa de Transporte HTTP (`src/app/api/`)
- **Herramienta:** `aws-lambda-powertools.event_handler.APIGatewayHttpResolver`.
- **Qué debe hacer:**
  - Extraer parámetros de ruta, query strings y body (`router.current_event.json_body`).
  - Instanciar y validar el DTO de entrada con Pydantic.
  - Llamar al método correspondiente del servicio (`Service`).
  - Capturar excepciones de dominio y mapearlas a excepciones HTTP de Powertools (`NotFoundError`, `BadRequestError`).
  - Devolver códigos HTTP semánticos (`200`, `201`, etc.).
- **Buenas prácticas:**
  - No escribir sentencias SQL ni manipular la base de datos directamente en las rutas.
  - No implementar cálculos o reglas de negocio dentro de los controladores.
  - Reutilizar la instancia del servicio a nivel de módulo para optimizar *warm starts*.

---

### 2. Capa de Contratos y DTOs (`src/app/schemas/`)
- **Herramienta:** `pydantic` v2 (`BaseModel`, `Field`, `ConfigDict`).
- **Qué debe hacer:**
  - Definir esquemas para solicitudes (`XCreateRequest`, `XUpdateRequest`).
  - Definir esquemas para respuestas (`XResponse`, `XListResponse`).
  - Aplicar validaciones de tipos, longitudes mínimas/máximas y valores positivos.
- **Buenas prácticas:**
  - Usar `model_config = ConfigDict(from_attributes=True)` para permitir la construcción desde objetos o tuplas.
  - No acoplar los DTOs a conceptos específicos de SQL ni a cabeceras HTTP.

---

### 3. Capa de Lógica de Negocio (`src/app/services/`)
- **Qué debe hacer:**
  - Contener la lógica de negocio pura y la orquestación de casos de uso (ej. generación de UUIDs, validación de duplicados, cálculo de precios o estados).
  - Recibir el repositorio mediante inyección de dependencias en el constructor:
    ```python
    def __init__(self, repository: UserRepositoryProtocol | None = None):
        self.repository = repository or UserRepository()
    ```
  - Lanzar **excepciones de dominio** (`ItemNotFoundError`, `AppException`, etc.) ante condiciones anómalas.
- **Buenas prácticas:**
  - Mantener los servicios 100% agnósticos al protocolo HTTP (no importar nada de `aws_lambda_powertools` ni retornar tuplas `(payload, 404)`).
  - No importar librerías de base de datos (`turso_serverless`) en los servicios; interactuar siempre a través de la interfaz del repositorio.

---

### 4. Capa de Persistencia (`src/app/repositories/`)
- **Herramienta:** `turso-serverless` sobre HTTPS.
- **Qué debe hacer:**
  - Definir la interfaz abstracta con `typing.Protocol` en `src/app/repositories/base.py`.
  - Implementar la clase concreta en `src/app/repositories/<name>_repository.py`.
  - Ejecutar consultas SQL utilizando parámetros seguros (`?`).
  - Mapear las filas resultantes a los DTOs de salida.
  - Incluir método `init_table()` con `CREATE TABLE IF NOT EXISTS` para DDL seguro.
- **Buenas prácticas:**
  - Permitir inyectar `connection_factory` en `__init__` para facilitar el mocking en pruebas.
  - No colocar validaciones de negocio en el repositorio; el repositorio solo persiste y recupera datos.

---

### 5. Capa Transversal (`src/app/core/`)
- **`exceptions.py`:** Jerarquía de excepciones de dominio heredando de `AppException`.
- **`config.py`:** Recupera credenciales desde AWS Secrets Manager (producción con caché) o variables locales (`.env`).
- **`database.py`:** Gestiona la conexión singleton a Turso abierta fuera del handler para reutilización en *warm starts*.
