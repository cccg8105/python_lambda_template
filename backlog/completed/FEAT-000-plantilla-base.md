# FEAT-000: Plantilla Base Serverless (Items + Turso + API Gateway)

| Metadato | Valor |
| :--- | :--- |
| **ID** | `FEAT-000` |
| **Tipo** | Feature / Arquitectura Base |
| **Versión Entregada** | `v0.1.0` |
| **Estado** | `Completado` |
| **Autor** | Equipo de Desarrollo |
| **Fecha de Creación** | 2026-10-23 |
| **Fecha de Finalización** | 2026-10-23 |

---

## 1. Historia de Usuario

> **Como** equipo de ingeniería  
> **Quiero** disponer de una plantilla de producción en Python 3.13 con Clean Architecture desacoplada  
> **Para** desarrollar funciones AWS Lambda conectadas a Turso Serverless con testing automatizado y SAM.

---

## 2. Criterios de Aceptación Cumplidos

- [x] Arquitectura en capas desacoplada (Router, Service, Repository, DTOs, Core).
- [x] Enrutamiento con AWS Lambda Powertools `APIGatewayHttpResolver` (Payload Format 2.0).
- [x] Driver `turso-serverless` con conexión persistente reutilizable en *warm starts*.
- [x] Validación estricta con Pydantic v2.
- [x] Configuración dinámica con AWS Secrets Manager y fallback a `.env`.
- [x] 100% de pruebas unitarias e integración en verde con `pytest`.
- [x] Plantilla AWS SAM `template.yaml` validada con `sam validate --lint`.
- [x] Suite de documentación en `docs/`.

---

## 3. Resumen de Entregables

- **Endpoints:** `GET /health`, `POST /admin/init-db`, `POST /items`, `GET /items`, `GET /items/<id>`, `PUT /items/<id>`, `DELETE /items/<id>`.
- **Entidades:** `Item`.
- **Base de datos:** Tabla `items` en Turso con SQL parametrizado.
- **Tests:** 18 pruebas automatizadas passing.
