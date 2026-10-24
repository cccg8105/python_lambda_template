# 📌 Backlog de Funcionalidades Pendientes (Roadmap)

Este documento centraliza el listado de todos los requerimientos pendientes por desarrollar, su prioridad y la **versión objetivo** a la cual están asignados.

---

## 🗺️ Requerimientos Planificados por Versión

### Hito: Versión `v0.2.0` (Gestión de Usuarios y Perfiles)

| ID | Requerimiento / Feature | Tipo | Prioridad | Estado | Enlace al Detalle |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FEAT-001** | Módulo de Gestión de Usuarios (CRUD) | `Feature` | Alta | ⏳ `Pendiente` | [Ver Especificación](FEAT-001-usuarios-crud.md) |

---

### Hito: Versión `v0.3.0` (Seguridad y Resiliencia) *(Propuestos)*

| ID | Requerimiento / Feature | Tipo | Prioridad | Estado | Enlace al Detalle |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FEAT-002** | Autenticación y Autorización vía JWT | `Feature` | Alta | 📝 *Por redactar* | - |
| **TECH-001** | Rate Limiting y Throttling en API Gateway | `Tech` | Media | 📝 *Por redactar* | - |

---

## ➕ Cómo Registrar un Nuevo Requerimiento

1. Crea una copia de [`../TEMPLATE.md`](../TEMPLATE.md) dentro de esta carpeta (`backlog/pending/`).
2. Nómbralo siguiendo el estándar: `FEAT-XXX-nombre-corto.md` (o `TECH-XXX` / `FIX-XXX`).
3. Diligencia la historia de usuario, criterios de aceptación y versión estimada.
4. Agrega una nueva fila en la tabla de este archivo con el enlace correspondiente.

---

## 🚀 Cómo Empezar a Implementar un Requerimiento

Al tomar un requerimiento de esta lista para iniciar su desarrollo:
1. **Crear la rama temática a partir de `main`:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/FEAT-XXX-slug
   ```
2. Sigue la [Guía de Desarrollo](../../docs/development-guide.md) paso a paso.
3. Asegura el 100% de tests (`uv run pytest -v`) antes de solicitar merge hacia `main`.

