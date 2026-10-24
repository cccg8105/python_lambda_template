"""Pruebas unitarias para la capa de repositorios."""

from unittest.mock import MagicMock

from app.repositories.item_repository import ItemRepository


def create_mock_connection():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # Context manager protocol for cursor
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_conn, mock_cursor


def test_init_table_executes_ddl():
    mock_conn, mock_cursor = create_mock_connection()
    repo = ItemRepository(connection_factory=lambda: mock_conn)

    repo.init_table()

    assert mock_cursor.execute.called
    query_executed = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS items" in query_executed
    assert mock_conn.commit.called


def test_save_inserts_and_commits():
    mock_conn, mock_cursor = create_mock_connection()
    repo = ItemRepository(connection_factory=lambda: mock_conn)

    item = repo.save(
        item_id="id-123",
        name="Monitor 4K",
        price=450.0,
        description="Monitor para desarrollo",
    )

    assert item.id == "id-123"
    assert item.name == "Monitor 4K"
    assert item.price == 450.0
    assert mock_cursor.execute.called
    query_executed, params = mock_cursor.execute.call_args[0]
    assert "INSERT INTO items" in query_executed
    assert params[0] == "id-123"
    assert params[1] == "Monitor 4K"
    assert mock_conn.commit.called


def test_find_by_id_returns_item_when_exists():
    mock_conn, mock_cursor = create_mock_connection()
    mock_cursor.fetchone.return_value = (
        "id-123",
        "Monitor 4K",
        450.0,
        "Monitor para desarrollo",
        "2026-10-23T10:00:00Z",
    )
    repo = ItemRepository(connection_factory=lambda: mock_conn)

    item = repo.find_by_id("id-123")

    assert item is not None
    assert item.id == "id-123"
    assert item.price == 450.0


def test_find_by_id_returns_none_when_not_found():
    mock_conn, mock_cursor = create_mock_connection()
    mock_cursor.fetchone.return_value = None
    repo = ItemRepository(connection_factory=lambda: mock_conn)

    item = repo.find_by_id("missing-id")

    assert item is None


def test_find_all_returns_list():
    mock_conn, mock_cursor = create_mock_connection()
    mock_cursor.fetchall.return_value = [
        ("id-1", "Item 1", 10.0, None, "2026-10-23T10:00:00Z"),
        ("id-2", "Item 2", 20.0, None, "2026-10-23T10:05:00Z"),
    ]
    repo = ItemRepository(connection_factory=lambda: mock_conn)

    items = repo.find_all(limit=10, offset=0)

    assert len(items) == 2
    assert items[0].id == "id-1"
    assert items[1].id == "id-2"


def test_delete_returns_true_when_found():
    mock_conn, mock_cursor = create_mock_connection()
    # Mock find_by_id to return an existing item
    mock_cursor.fetchone.return_value = ("id-1", "Item 1", 10.0, None, "2026-10-23")
    repo = ItemRepository(connection_factory=lambda: mock_conn)

    deleted = repo.delete("id-1")

    assert deleted is True
    assert mock_conn.commit.called
