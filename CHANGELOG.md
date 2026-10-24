# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### Planned (v0.2.0)
- **FEAT-001**: Módulo de gestión de usuarios CRUD con validación de email único ([Detalle](backlog/pending/FEAT-001-usuarios-crud.md)).

---

## [0.1.0] - 2026-10-23

### Added
- **FEAT-000**: Plantilla base desacoplada para AWS Lambda con Python 3.13.9 y arquitectura en capas ([Detalle](backlog/completed/FEAT-000-plantilla-base.md)).
- Integración con API Gateway HTTP API (Payload Format 2.0) mediante `aws-lambda-powertools` `APIGatewayHttpResolver`.
- Persistencia con base de datos serverless Turso (libSQL) a través del driver `turso-serverless` sobre HTTPS.
- Validación de contratos y DTOs fuertemente tipados con Pydantic v2.
- Resolución de credenciales con AWS Secrets Manager (caché TTL 5 min) y fallback local a `.env`.
- Entidad `Item` con operaciones CRUD completas y endpoint `/health`.
- Plantilla AWS SAM `template.yaml` para despliegues en arquitectura `arm64`.
- Suite completa de documentación técnica en carpeta `docs/`.
- Sistema de gestión de backlog ágil en carpeta `backlog/` con soporte para Trunk-Based Development.
