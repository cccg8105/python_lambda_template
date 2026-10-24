"""Controladores HTTP para la gestión de Items."""

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Response
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError
from pydantic import ValidationError

from app.api.router import router
from app.core.exceptions import ItemNotFoundError
from app.schemas.item import ItemCreateRequest, ItemUpdateRequest
from app.services.item_service import ItemService

logger = Logger(child=True)

# Instancia del servicio reutilizable durante warm starts
item_service = ItemService()


@router.post("/items")
def create_item():
    """Crea un nuevo item a partir del payload JSON."""
    raw_body = router.current_event.json_body
    if not raw_body:
        raise BadRequestError("Cuerpo de solicitud vacío o JSON inválido.")

    try:
        dto = ItemCreateRequest(**raw_body)
    except ValidationError as exc:
        raise BadRequestError(str(exc))

    created = item_service.create_item(dto)
    return Response(
        status_code=201,
        content_type="application/json",
        body=created.model_dump_json(),
    )


@router.get("/items")
def list_items() -> dict:
    """Lista items existentes con paginación opcional."""
    query_params = router.current_event.query_string_parameters or {}
    try:
        limit = int(query_params.get("limit", 50))
        offset = int(query_params.get("offset", 0))
    except ValueError:
        raise BadRequestError("Los parámetros 'limit' y 'offset' deben ser números enteros.")

    result = item_service.list_items(limit=limit, offset=offset)
    return result.model_dump()


@router.get("/items/<item_id>")
def get_item(item_id: str) -> dict:
    """Obtiene el detalle de un item por su ID."""
    try:
        item = item_service.get_item(item_id)
        return item.model_dump()
    except ItemNotFoundError as exc:
        raise NotFoundError(str(exc))


@router.put("/items/<item_id>")
def update_item(item_id: str) -> dict:
    """Actualiza un item existente."""
    raw_body = router.current_event.json_body
    if not raw_body:
        raise BadRequestError("Cuerpo de solicitud vacío o JSON inválido.")

    try:
        dto = ItemUpdateRequest(**raw_body)
    except ValidationError as exc:
        raise BadRequestError(str(exc))

    try:
        updated = item_service.update_item(item_id, dto)
        return updated.model_dump()
    except ItemNotFoundError as exc:
        raise NotFoundError(str(exc))


@router.delete("/items/<item_id>")
def delete_item(item_id: str) -> dict:
    """Elimina un item por su ID."""
    try:
        item_service.delete_item(item_id)
        return {"message": f"Item '{item_id}' eliminado con éxito."}
    except ItemNotFoundError as exc:
        raise NotFoundError(str(exc))
