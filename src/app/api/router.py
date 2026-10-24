"""Instancia principal del enrutador HTTP de Powertools para API Gateway v2."""

from aws_lambda_powertools.event_handler import APIGatewayHttpResolver

# Resolver para API Gateway HTTP API (Payload Format 2.0)
router = APIGatewayHttpResolver(enable_validation=True)
