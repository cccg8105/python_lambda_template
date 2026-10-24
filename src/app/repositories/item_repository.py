"""Implementación del repositorio de Items utilizando turso_serverless."""

from collections.abc import Callable
from datetime import UTC, datetime

from aws_lambda_powertools import Logger

from app.core.database import get_turso_connection
from app.schemas.item import ItemResponse

logger = Logger(child=True)


class ItemRepository:
    """Repositorio de persistencia que ejecuta SQL parametrizado sobre Turso."""

    def __init__(self, connection_factory: Callable | None = None):
        self._get_connection = connection_factory or get_turso_connection

    def init_table(self) -> None:
        """Crea la tabla 'items' en Turso si aún no existe."""
        conn = self._get_connection()
        query = """
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL
        );
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
        logger.info("Tabla 'items' verificada/inicializada en Turso.")

    def save(
        self,
        item_id: str,
        name: str,
        price: float,
        description: str | None = None,
        created_at: str | None = None,
    ) -> ItemResponse:
        """Inserta un nuevo item en Turso y retorna su DTO."""
        if not created_at:
            created_at = datetime.now(UTC).isoformat()

        conn = self._get_connection()
        query = """
        INSERT INTO items (id, name, price, description, created_at)
        VALUES (?, ?, ?, ?, ?);
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (item_id, name, price, description, created_at))
            conn.commit()

        return ItemResponse(
            id=item_id,
            name=name,
            price=price,
            description=description,
            created_at=created_at,
        )

    def find_by_id(self, item_id: str) -> ItemResponse | None:
        """Obtiene un item por ID o None si no existe."""
        conn = self._get_connection()
        query = "SELECT id, name, price, description, created_at FROM items WHERE id = ?;"
        with conn.cursor() as cursor:
            cursor.execute(query, (item_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return ItemResponse(
                id=row[0],
                name=row[1],
                price=float(row[2]),
                description=row[3],
                created_at=row[4],
            )

    def find_all(self, limit: int = 50, offset: int = 0) -> list[ItemResponse]:
        """Retorna una lista de items ordenada por fecha descendente."""
        conn = self._get_connection()
        query = """
        SELECT id, name, price, description, created_at
        FROM items
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?;
        """
        items: list[ItemResponse] = []
        with conn.cursor() as cursor:
            cursor.execute(query, (limit, offset))
            for row in cursor.fetchall():
                items.append(
                    ItemResponse(
                        id=row[0],
                        name=row[1],
                        price=float(row[2]),
                        description=row[3],
                        created_at=row[4],
                    )
                )
        return items

    def update(
        self,
        item_id: str,
        name: str | None = None,
        price: float | None = None,
        description: str | None = None,
    ) -> ItemResponse | None:
        """Actualiza campos de un item existente."""
        current = self.find_by_id(item_id)
        if not current:
            return None

        new_name = name if name is not None else current.name
        new_price = price if price is not None else current.price
        new_description = description if description is not None else current.description

        conn = self._get_connection()
        query = """
        UPDATE items
        SET name = ?, price = ?, description = ?
        WHERE id = ?;
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (new_name, new_price, new_description, item_id))
            conn.commit()

        return ItemResponse(
            id=item_id,
            name=new_name,
            price=new_price,
            description=new_description,
            created_at=current.created_at,
        )

    def delete(self, item_id: str) -> bool:
        """Elimina un item y devuelve True si fue eliminado."""
        if not self.find_by_id(item_id):
            return False

        conn = self._get_connection()
        query = "DELETE FROM items WHERE id = ?;"
        with conn.cursor() as cursor:
            cursor.execute(query, (item_id,))
            conn.commit()
        return True
