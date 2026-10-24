"""Rutas para verificación de salud y utilidades del sistema."""

from datetime import UTC, datetime

from app.api.router import router
from app.repositories.item_repository import ItemRepository


@router.get("/")
@router.get("/health")
def health_check() -> dict:
    """Endpoint de comprobación de salud para monitoreo."""
    return {
        "status": "healthy",
        "service": "turso-api-service",
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.post("/admin/init-db")
def initialize_database() -> dict:
    """Endpoint de utilidad para crear las tablas necesarias en Turso si aún no existen."""
    repo = ItemRepository()
    repo.init_table()
    return {"message": "Tabla 'items' inicializada correctamente en Turso."}
