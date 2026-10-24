"""Protocolos e interfaces de persistencia."""

from typing import Protocol

from app.schemas.item import ItemResponse


class ItemRepositoryProtocol(Protocol):
    """Contrato que define los métodos que debe implementar cualquier repositorio de Items."""

    def init_table(self) -> None:
        """Inicializa la tabla en la base de datos si no existe."""
        ...

    def save(
        self,
        item_id: str,
        name: str,
        price: float,
        description: str | None = None,
        created_at: str | None = None,
    ) -> ItemResponse:
        """Guarda un nuevo item."""
        ...

    def find_by_id(self, item_id: str) -> ItemResponse | None:
        """Busca un item por su ID."""
        ...

    def find_all(self, limit: int = 50, offset: int = 0) -> list[ItemResponse]:
        """Obtiene una lista de items."""
        ...

    def update(
        self,
        item_id: str,
        name: str | None = None,
        price: float | None = None,
        description: str | None = None,
    ) -> ItemResponse | None:
        """Actualiza un item existente."""
        ...

    def delete(self, item_id: str) -> bool:
        """Elimina un item por su ID."""
        ...
