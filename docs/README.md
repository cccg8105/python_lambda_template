# Documentación Técnica del Proyecto

¡Bienvenido a la documentación de desarrollo de **Python Lambda Turso Template**!

Esta carpeta contiene las guías de diseño, arquitectura, persistencia y lineamientos de desarrollo para cualquier desarrollador que se incorpore al equipo o desee extender las funcionalidades del proyecto.

---

## 🗺️ Mapa de Navegación

| Documento | Descripción | Audiencia / Objetivo |
| :--- | :--- | :--- |
| **[architecture.md](architecture.md)** | Diseño arquitectónico en capas (Clean Architecture), responsabilidades de cada módulo y diagramas de flujo de peticiones. | Comprender cómo fluyen los datos y por qué está estructurado el código de esta manera. |
| **[development-guide.md](development-guide.md)** | Guía práctica paso a paso para crear un nuevo recurso de principio a fin utilizando como ejemplo la entidad `User`. | Nuevos desarrollos y recetas copy-pasteable de código. |
| **[database-turso.md](database-turso.md)** | Funcionamiento del cliente `turso-serverless`, SQL sobre HTTPS, ciclo de vida en AWS Lambda (*warm starts* vs *cold starts*) y buenas prácticas de consultas. | Consultas de base de datos, DDL y persistencia. |
| **[api-conventions.md](api-conventions.md)** | Convenciones de API Gateway HTTP API v2, códigos de estado HTTP, validación con Pydantic v2 y manejo de excepciones. | Diseño de contratos, endpoints y respuestas JSON. |
| **[testing-guide.md](testing-guide.md)** | Estrategia de testing, mocking de capas, emulación de eventos de API Gateway v2 y ejecución con `pytest`. | Escribir pruebas unitarias e integrales para nuevo código. |

---

## 🚀 Inicio Rápido para Nuevos Desarrolladores

1. **Requisitos de entorno:**
   - Asegúrate de tener instalado [uv](https://docs.astral.sh/uv/) y [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
   - El proyecto utiliza **Python 3.13.9** (fijado automáticamente por `.python-version`).

2. **Configurar el entorno local:**
   ```bash
   uv venv --python 3.13.9
   uv sync
   cp .env.example .env
   ```

3. **Verificar que todo funciona:**
   ```bash
   uv run pytest -v
   uv run ruff check .
   ```

4. **Siguiente paso recomendado:**
   Lee la [Guía de Arquitectura](architecture.md) para entender la división de capas antes de escribir código.
