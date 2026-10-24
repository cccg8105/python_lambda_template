# Python Lambda Turso Template

Plantilla de producción para funciones **AWS Lambda** escritas en **Python 3.13**, expuestas mediante **API Gateway HTTP API (Payload Format 2.0)** y conectadas a la base de datos serverless **Turso (libSQL)** utilizando el driver DB-API 2.0 `turso-serverless`.

La plantilla implementa **Clean Architecture / Arquitectura en Capas** para separar estrictamente el transporte HTTP, la validación de contratos, la lógica de negocio y el acceso a datos.

---

## 🏛️ Arquitectura del Proyecto

```text
src/app/
├── main.py                  # Entrypoint de AWS Lambda (lambda_handler)
├── api/                     # CAPA 1: Transporte y Enrutamiento (Powertools APIGatewayHttpResolver)
│   ├── router.py            # Instancia central del enrutador
│   └── routes/              # Controladores HTTP (items, health)
├── schemas/                 # CAPA 2: Contratos y DTOs (Pydantic v2)
│   └── item.py              # Esquemas fuertemente tipados
├── services/                # CAPA 3: Lógica de Negocio (ItemService)
│   └── item_service.py      # Casos de uso desacoplados de HTTP y SQL
├── repositories/            # CAPA 4: Persistencia (ItemRepository)
│   ├── base.py              # Protocol/Interface de acceso a datos
│   └── item_repository.py   # Consultas SQL parametrizadas sobre Turso
└── core/                    # CAPA TRANSVERSAL: Configuración y conexión
    ├── config.py            # AWS Secrets Manager con fallback a variables de entorno
    ├── database.py          # Singleton de conexión DB-API con turso_serverless
    └── exceptions.py        # Excepciones de dominio
```

---

## 📚 Documentación Técnica Detallada

Para guías completas de arquitectura, nuevos desarrollos y buenas prácticas, consulta la carpeta [`docs/`](docs/README.md):

- 🏛️ **[Arquitectura y Diseño en Capas](docs/architecture.md)**: Flujo de peticiones, Clean Architecture y diagramas Mermaid.
- 🛠️ **[Guía para Nuevos Desarrollos](docs/development-guide.md)**: Tutorial paso a paso para crear un nuevo recurso (`User`) de 0 a 1.
- ⚡ **[Turso Serverless & Persistencia](docs/database-turso.md)**: Conexión sobre HTTPS, warm starts, DDL y consultas seguras.
- 🚦 **[Convenciones de API y Contratos](docs/api-conventions.md)**: Payload format 2.0, códigos HTTP y serialización Pydantic v2.
- 🧪 **[Guía de Testing](docs/testing-guide.md)**: Mocks, fixtures, emulación de API Gateway y ejecución de tests.

---

## 📋 Gestión del Backlog y Versionamiento

El proyecto cuenta con un sistema ágil para la planificación y entrega continua de funcionalidades:

- 📌 **[Roadmap / Backlog Pendiente](backlog/pending/README.md)**: Listado de funcionalidades por implementar y versión objetivo asignada.
- 🏁 **[Historial de Features Completados](backlog/completed/README.md)**: Registro de requerimientos finalizados organizados por versión de entrega.
- 🌳 **[Estrategia de Versionamiento (SemVer & Trunk-Based)](backlog/VERSIONING.md)**: Flujo de ramas, Conventional Commits y releases.
- 📝 **[Plantilla Ágil de Requerimientos](backlog/TEMPLATE.md)**: Formato estándar para nuevas historias de usuario y DoD.
- 📜 **[CHANGELOG.md](CHANGELOG.md)**: Historial formal de cambios por versión.

---

## 🤖 Reglas y Directrices de Antigravity

El repositorio incluye directrices para que los asistentes de IA mantengan la consistencia y respeten la arquitectura del proyecto:

- 📋 **[GEMINI.md](GEMINI.md)**: Reglas maestras del proyecto (cargadas automáticamente por Antigravity).
- 🏛️ **[.agents/rules/architecture.md](.agents/rules/architecture.md)**: Convenciones de Clean Architecture y responsabilidades por capa.
- ⚡ **[.agents/rules/database.md](.agents/rules/database.md)**: Conexión con Turso Serverless, warm starts y consultas seguras.
- 🧪 **[.agents/rules/quality.md](.agents/rules/quality.md)**: Tipado moderno en Python 3.13, verificación con pytest y ruff.
- 🌳 **[.agents/rules/workflow.md](.agents/rules/workflow.md)**: Trunk-Based Development, Conventional Commits y ciclo del backlog.

---



## 🚀 Requisitos Previos

- [uv](https://docs.astral.sh/uv/) (Gestor de entornos y paquetes ultrarrápido)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.13 (fijado automáticamente por `.python-version`)

---

## 🛠️ Instalación y Configuración Local

1. **Crear el entorno virtual e instalar dependencias:**
   ```bash
   uv venv --python 3.13.9
   uv sync
   ```

2. **Configurar variables de entorno locales:**
   Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```
   Edita `.env` con tus credenciales de Turso:
   ```env
   TURSO_DATABASE_URL=libsql://tu-base-de-datos.turso.io
   TURSO_AUTH_TOKEN=tu-token-aqui
   AWS_SAM_LOCAL=true
   ```

---

## 🧪 Ejecución de Pruebas

Ejecutar la suite completa de pruebas unitarias y de integración:

```bash
uv run pytest -v
```

---

## ☁️ Pruebas Locales y Despliegue con AWS SAM

1. **Validar la plantilla SAM:**
   ```bash
   sam validate --lint
   ```

2. **Iniciar la API localmente:**
   ```bash
   sam local start-api --env-vars env.json
   ```

3. **Construir y desplegar a AWS:**
   ```bash
   sam build
   sam deploy --guided
   ```

---

## 🔐 Gestión de Secretos en Producción

En AWS, la función recupera las credenciales de Turso de forma automática y segura utilizando **AWS Secrets Manager** a través de `aws-lambda-powertools` Parameters (con caché de 5 minutos):

- Secreto por defecto: `prod/turso/credentials`
- Formato esperado en Secrets Manager (JSON):
  ```json
  {
    "database_url": "libsql://tu-base-de-datos.turso.io",
    "auth_token": "tu-turso-auth-token"
  }
  ```
