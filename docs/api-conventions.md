# Convenciones de API y Contratos HTTP

Este documento establece las convenciones de diseño para la API expuesta a través de **API Gateway HTTP API (Payload Format 2.0)**.

---

## 🌐 Formato de Evento: Payload Format 2.0

La aplicación utiliza la versión 2.0 de payloads de API Gateway HTTP API, caracterizada por:
- Estructura JSON simplificada en `requestContext.http`.
- Cabeceras normalizadas en minúsculas.
- Soporte nativo para rutas dinámicas (`/items/{item_id}`).
- Procesamiento eficiente a través de `APIGatewayHttpResolver` de Powertools.

---

## 🚦 Códigos de Estado HTTP y Semántica

| Código | Significado | Cuándo usarlo en el proyecto |
| :--- | :--- | :--- |
| **`200 OK`** | Éxito | Consultas `GET` exitosas, actualizaciones `PUT` y eliminaciones `DELETE`. |
| **`201 Created`** | Recurso Creado | Operaciones `POST` que crean una nueva entidad con éxito. Debe retornar el objeto creado. |
| **`400 Bad Request`** | Error del Cliente | Validación fallida de Pydantic (tipos, campos requeridos) o violaciones de reglas de negocio (ej. email duplicado). |
| **`404 Not Found`** | Recurso No Encontrado | Cuando un ID solicitado no existe en la base de datos (`ItemNotFoundError`). |
| **`500 Internal Server Error`** | Error del Servidor | Excepciones no controladas o fallos inesperados de infraestructura (fallo de red en Secrets Manager, etc.). |

---

## 📐 Estándares de Datos y Serialización

### 1. Formato de Fechas
Todas las fechas deben serializarse en formato **ISO-8601 UTC**:
```json
"created_at": "2026-10-23T19:30:00.000000+00:00"
```

### 2. Identificadores Únicos
Todos los identificadores primarios son cadenas **UUIDv4**:
```json
"id": "a5c7f89b-8105-4c92-b43e-389d38c6e80b"
```

### 3. Respuestas de Listados Paginados
Las respuestas de colecciones deben seguir una estructura consistente con el array de elementos y el conteo total:
```json
{
  "items": [
    {
      "id": "...",
      "name": "...",
      "price": 100.0,
      "description": "...",
      "created_at": "..."
    }
  ],
  "total": 1
}
```

---

## ⚠️ Mapeo de Excepciones

La capa de enrutamiento (`src/app/api/routes/`) es responsable de atrapar las excepciones de dominio y traducirlas a excepciones HTTP de Powertools:

```python
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError
from pydantic import ValidationError
from app.core.exceptions import ItemNotFoundError

# 1. Error de validación sintáctica (Pydantic)
try:
    dto = ItemCreateRequest(**raw_body)
except ValidationError as exc:
    raise BadRequestError(str(exc))

# 2. Error de recurso inexistente (Dominio)
try:
    item = item_service.get_item(item_id)
    return item.model_dump()
except ItemNotFoundError as exc:
    raise NotFoundError(str(exc))
```

Powertools serializa automáticamente estas excepciones en respuestas estándar:
```json
{
  "statusCode": 404,
  "message": "Item con id '123' no encontrado."
}
```

---

## 🌍 Política CORS (Cross-Origin Resource Sharing)

CORS está configurado a nivel de infraestructura en [template.yaml](file:///c:/Users/cesar/repos/python_lambda_template/template.yaml):
- **Orígenes permitidos:** `*` (o restringir según dominio frontend en producción).
- **Métodos permitidos:** `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`.
- **Cabeceras permitidas:** `Content-Type`, `Authorization`, `X-Correlation-Id`.

---

## 🔍 Trazabilidad y Correlación (`X-Correlation-Id`)

Cada solicitud que procesa la API genera un identificador único **UUIDv4** para trazabilidad de extremo a extremo:

- **Cabecera de respuesta:** Toda respuesta HTTP incluye la cabecera `X-Correlation-Id`.
- **Logs estructurados:** El identificador se adjunta automáticamente a todos los eventos emitidos por el Logger de Powertools durante el ciclo de vida de la petición.
- **Soporte y diagnóstico:** Si un cliente o consumidor experimenta un fallo, el valor de `X-Correlation-Id` permite filtrar y ubicar en segundos la traza completa de la petición en AWS CloudWatch Logs Insights.
