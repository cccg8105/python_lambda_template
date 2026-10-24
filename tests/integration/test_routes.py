"""Pruebas de integración de rutas de API Gateway v2 y lambda_handler."""

import json
from unittest.mock import patch

from app.main import lambda_handler
from app.schemas.item import ItemResponse


def build_apigw_v2_event(
    http_method: str,
    path: str,
    body: dict | None = None,
    query_params: dict | None = None,
) -> dict:
    """Construye un evento sintético que emula API Gateway HTTP API (Payload Format 2.0)."""
    return {
        "version": "2.0",
        "routeKey": f"{http_method} {path}",
        "rawPath": path,
        "rawQueryString": "",
        "headers": {
            "content-type": "application/json",
            "host": "api.example.com",
        },
        "queryStringParameters": query_params or {},
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "r3pmxmplab",
            "domainName": "api.example.com",
            "domainPrefix": "api",
            "http": {
                "method": http_method,
                "path": path,
                "protocol": "HTTP/1.1",
                "sourceIp": "127.0.0.1",
                "userAgent": "pytest/1.0",
            },
            "requestId": "JKJaXmPLvHcESHA=",
            "routeKey": f"{http_method} {path}",
            "stage": "$default",
            "time": "23/Oct/2026:19:00:00 +0000",
            "timeEpoch": 1792782000000,
        },
        "body": json.dumps(body) if body is not None else None,
        "isBase64Encoded": False,
    }


def test_health_check_route(lambda_context):
    event = build_apigw_v2_event("GET", "/health")
    response = lambda_handler(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["status"] == "healthy"
    assert body["service"] == "turso-api-service"


def test_create_item_valid_payload(lambda_context):
    event = build_apigw_v2_event(
        "POST",
        "/items",
        body={"name": "Auriculares Bluetooth", "price": 49.99, "description": "Con cancelación"},
    )

    with patch("app.api.routes.items.item_service.create_item") as mock_create:
        mock_create.return_value = ItemResponse(
            id="mock-uuid-999",
            name="Auriculares Bluetooth",
            price=49.99,
            description="Con cancelación",
            created_at="2026-10-23T19:00:00Z",
        )

        response = lambda_handler(event, lambda_context)

        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert body["id"] == "mock-uuid-999"
        assert body["name"] == "Auriculares Bluetooth"
        assert body["price"] == 49.99


def test_create_item_invalid_payload_returns_400(lambda_context):
    # Precio negativo inválido
    event = build_apigw_v2_event(
        "POST",
        "/items",
        body={"name": "Item Inválido", "price": -10.0},
    )

    response = lambda_handler(event, lambda_context)

    assert response["statusCode"] == 400


def test_get_item_not_found_returns_404(lambda_context):
    event = build_apigw_v2_event("GET", "/items/non-existent-id")

    with patch("app.api.routes.items.item_service.get_item") as mock_get:
        from app.core.exceptions import ItemNotFoundError

        mock_get.side_effect = ItemNotFoundError("Item inexistente")

        response = lambda_handler(event, lambda_context)

        assert response["statusCode"] == 404
