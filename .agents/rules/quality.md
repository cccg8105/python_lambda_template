# Reglas de Calidad de Código, Tipado y Testing

Este documento establece las directrices de calidad, estilo de código y pruebas automatizadas que deben cumplirse en todo el repositorio.

---

## 🐍 Tipado Moderno en Python 3.13

El proyecto utiliza **Python 3.13.9** gestionado con `uv`. Se deben aplicar las sintaxis de tipado modernas introducidas en las versiones recientes de Python:

| Sintaxis Antigua (Evitar) | Sintaxis Moderna Python 3.13 (Usar) |
| :--- | :--- |
| `from typing import Optional; Optional[str]` | `str | None` |
| `from typing import Union; Union[int, str]` | `int | str` |
| `from typing import List; List[ItemResponse]` | `list[ItemResponse]` |
| `from typing import Dict; Dict[str, Any]` | `dict[str, Any]` |
| `from typing import Set; Set[str]` | `set[str]` |

---

## 🧪 Estrategia y Estructura de Pruebas

Toda nueva funcionalidad o cambio de comportamiento debe estar respaldado por pruebas:

1. **Pruebas Unitarias de Servicios (`tests/unit/`):**
   - Probar casos de éxito y de error (ej. excepciones de dominio esperadas).
   - Sustituir los repositorios por `unittest.mock.MagicMock`.
   - **No realizar llamadas de red ni acceder a la base de datos real** durante las pruebas unitarias.

2. **Pruebas Unitarias de Repositorios (`tests/unit/`):**
   - Evaluar que las consultas SQL parametrizadas se construyan con los parámetros esperados y se invoque `conn.commit()`.
   - Utilizar mocks del protocolo DB-API (`cursor`, `fetchone`, `fetchall`).

3. **Pruebas de Integración (`tests/integration/`):**
   - Invocar directamente a `lambda_handler(event, lambda_context)` usando la función auxiliar `build_apigw_v2_event(...)`.
   - Verificar los códigos de estado HTTP (`200`, `201`, `400`, `404`) y la correcta serialización del JSON en `response["body"]`.

4. **Variables de Entorno para Pruebas:**
   - Mantener las variables mock en `tests/conftest.py` (`AWS_SAM_LOCAL=true`, `TURSO_DATABASE_URL=...`) para aislar los tests de entornos de producción.

---

## 🚦 Criterios de Calidad (Quality Gates)

Antes de considerar una tarea completada, se deben ejecutar y aprobar los siguientes comandos:

1. **Ejecutar suite de pruebas completa:**
   ```bash
   uv run pytest -v
   ```
   *Debe superar el 100% de los tests sin fallos.*

2. **Verificar linter y formato:**
   ```bash
   uv run ruff check .
   uv run ruff format .
   ```
   *No debe arrojar errores ni advertencias de estilo.*

3. **Validar plantilla SAM (si se modificó `template.yaml`):**
   ```bash
   sam validate --lint
   ```
   *Debe confirmar que la plantilla es válida.*
