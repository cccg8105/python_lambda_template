"""Modelos y contratos de datos para la entidad Item."""

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    """Atributos comunes de un item."""

    name: str = Field(..., min_length=1, max_length=100, description="Nombre del item")
    price: float = Field(..., gt=0, description="Precio unitario (debe ser mayor a 0)")
    description: str | None = Field(
        default=None, max_length=500, description="Descripción opcional"
    )


class ItemCreateRequest(ItemBase):
    """Payload para creación de un item."""


class ItemUpdateRequest(BaseModel):
    """Payload para actualización parcial de un item."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, max_length=500)


class ItemResponse(ItemBase):
    """DTO de respuesta con el item completo."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Identificador único (UUID)")
    created_at: str | None = Field(default=None, description="Fecha de creación ISO-8601")


class ItemListResponse(BaseModel):
    """DTO para listados paginados de items."""

    items: list[ItemResponse]
    total: int
