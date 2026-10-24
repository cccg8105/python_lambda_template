"""Servicio de lógica de negocio para Items."""

import uuid

from aws_lambda_powertools import Logger

from app.core.exceptions import ItemNotFoundError
from app.repositories.base import ItemRepositoryProtocol
from app.repositories.item_repository import ItemRepository
from app.schemas.item import (
    ItemCreateRequest,
    ItemListResponse,
    ItemResponse,
    ItemUpdateRequest,
)

logger = Logger(child=True)


class ItemService:
    """Orquesta las reglas de negocio para los items."""

    def __init__(self, repository: ItemRepositoryProtocol | None = None):
        self.repository: ItemRepositoryProtocol = repository or ItemRepository()

    def create_item(self, dto: ItemCreateRequest) -> ItemResponse:
        """Crea un nuevo item asignándole un UUID único."""
        item_id = str(uuid.uuid4())
        cleaned_name = dto.name.strip()

        logger.info(f"Creando nuevo item: '{cleaned_name}' con ID {item_id}")
        return self.repository.save(
            item_id=item_id,
            name=cleaned_name,
            price=dto.price,
            description=dto.description.strip() if dto.description else None,
        )

    def get_item(self, item_id: str) -> ItemResponse:
        """Obtiene un item por ID o eleva ItemNotFoundError."""
        item = self.repository.find_by_id(item_id)
        if not item:
            raise ItemNotFoundError(f"Item con id '{item_id}' no encontrado.")
        return item

    def list_items(self, limit: int = 50, offset: int = 0) -> ItemListResponse:
        """Obtiene una lista de items paginada."""
        items = self.repository.find_all(limit=limit, offset=offset)
        return ItemListResponse(items=items, total=len(items))

    def update_item(self, item_id: str, dto: ItemUpdateRequest) -> ItemResponse:
        """Actualiza un item existente o eleva ItemNotFoundError."""
        cleaned_name = dto.name.strip() if dto.name is not None else None
        cleaned_desc = dto.description.strip() if dto.description is not None else None

        updated = self.repository.update(
            item_id=item_id,
            name=cleaned_name,
            price=dto.price,
            description=cleaned_desc,
        )
        if not updated:
            raise ItemNotFoundError(f"No se pudo actualizar: item '{item_id}' no encontrado.")
        return updated

    def delete_item(self, item_id: str) -> None:
        """Elimina un item por su ID o eleva ItemNotFoundError."""
        deleted = self.repository.delete(item_id)
        if not deleted:
            raise ItemNotFoundError(f"No se pudo eliminar: item '{item_id}' no encontrado.")
        logger.info(f"Item '{item_id}' eliminado correctamente.")
