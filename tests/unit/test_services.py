"""Pruebas unitarias para la capa de servicios (lógica de negocio)."""

from unittest.mock import MagicMock

import pytest

from app.core.exceptions import ItemNotFoundError
from app.schemas.item import ItemCreateRequest, ItemResponse, ItemUpdateRequest
from app.services.item_service import ItemService


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def item_service(mock_repository):
    return ItemService(repository=mock_repository)


def test_create_item_success(item_service, mock_repository):
    # Arrange
    req = ItemCreateRequest(name="  Laptop Pro  ", price=1299.99, description="Potente laptop")
    mock_repository.save.return_value = ItemResponse(
        id="mock-uuid-1234",
        name="Laptop Pro",
        price=1299.99,
        description="Potente laptop",
        created_at="2026-10-23T12:00:00Z",
    )

    # Act
    result = item_service.create_item(req)

    # Assert
    assert result.name == "Laptop Pro"
    assert result.price == 1299.99
    assert result.id == "mock-uuid-1234"
    mock_repository.save.assert_called_once()
    _args, kwargs = mock_repository.save.call_args
    assert kwargs["name"] == "Laptop Pro"  # Verifica el sanitize/strip
    assert kwargs["price"] == 1299.99


def test_get_item_found(item_service, mock_repository):
    # Arrange
    mock_repository.find_by_id.return_value = ItemResponse(
        id="item-1",
        name="Mouse Wireless",
        price=29.99,
        description=None,
        created_at="2026-10-23T12:00:00Z",
    )

    # Act
    result = item_service.get_item("item-1")

    # Assert
    assert result.id == "item-1"
    assert result.name == "Mouse Wireless"


def test_get_item_not_found_raises_exception(item_service, mock_repository):
    # Arrange
    mock_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ItemNotFoundError) as exc_info:
        item_service.get_item("non-existent-id")

    assert "no encontrado" in str(exc_info.value)


def test_list_items(item_service, mock_repository):
    # Arrange
    mock_repository.find_all.return_value = [
        ItemResponse(id="1", name="A", price=10.0),
        ItemResponse(id="2", name="B", price=20.0),
    ]

    # Act
    result = item_service.list_items(limit=10, offset=0)

    # Assert
    assert result.total == 2
    assert len(result.items) == 2
    mock_repository.find_all.assert_called_once_with(limit=10, offset=0)


def test_update_item_success(item_service, mock_repository):
    # Arrange
    dto = ItemUpdateRequest(name="Teclado Mecanico", price=89.5)
    mock_repository.update.return_value = ItemResponse(
        id="item-1",
        name="Teclado Mecanico",
        price=89.5,
    )

    # Act
    result = item_service.update_item("item-1", dto)

    # Assert
    assert result.name == "Teclado Mecanico"
    assert result.price == 89.5


def test_update_item_not_found_raises_exception(item_service, mock_repository):
    # Arrange
    dto = ItemUpdateRequest(name="Nuevo")
    mock_repository.update.return_value = None

    # Act & Assert
    with pytest.raises(ItemNotFoundError):
        item_service.update_item("item-inexistente", dto)


def test_delete_item_success(item_service, mock_repository):
    # Arrange
    mock_repository.delete.return_value = True

    # Act
    item_service.delete_item("item-1")

    # Assert
    mock_repository.delete.assert_called_once_with("item-1")


def test_delete_item_not_found_raises_exception(item_service, mock_repository):
    # Arrange
    mock_repository.delete.return_value = False

    # Act & Assert
    with pytest.raises(ItemNotFoundError):
        item_service.delete_item("item-inexistente")
