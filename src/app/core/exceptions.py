"""Excepciones de dominio y de infraestructura de la aplicación."""


class AppException(Exception):
    """Excepción base de la aplicación."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ItemNotFoundError(AppException):
    """Lanzada cuando un recurso no se encuentra en el repositorio."""


class ItemAlreadyExistsError(AppException):
    """Lanzada cuando se intenta crear un recurso con clave duplicada."""


class DatabaseConnectionError(AppException):
    """Lanzada ante fallos de conexión o configuración con Turso."""
