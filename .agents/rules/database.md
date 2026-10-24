# Reglas de Base de Datos y Persistencia con Turso

Este documento establece las pautas de interacción con **Turso Serverless (libSQL)** mediante el driver `turso-serverless`.

---

## ⚡ Conexión y Ciclo de Vida en Serverless

1. **Driver 100% Pure Python:**
   - Usar exclusivamente `turso-serverless` vía DB-API 2.0. No incorporar dependencias nativas o compiladas en C/Rust para evitar problemas de compatibilidad en entornos serverless.
   - Parámetros de conexión:
     ```python
     turso_serverless.connect(url=db_url, auth_token=auth_token)
     ```

2. **Reutilización de Conexión en Warm Starts:**
   - La conexión a Turso debe gestionarse como un singleton a nivel de módulo a través de `get_turso_connection()` en `src/app/core/database.py`.
   - **No instanciar conexiones dentro del cuerpo de la función Lambda ni dentro de bucles.** Inicializar la conexión fuera del handler para que las peticiones subsecuentes reutilicen la conexión ya abierta.

3. **Resolución Segura de Credenciales:**
   - En AWS Lambda: Utilizar `aws_lambda_powertools.utilities.parameters.get_secret` con caché (TTL de 300 segundos) para evitar costos y latencia innecesaria hacia Secrets Manager.
   - En desarrollo local: Leer automáticamente de `TURSO_DATABASE_URL` y `TURSO_AUTH_TOKEN` en variables de entorno o `.env`.

---

## 🛡️ Seguridad y Buenas Prácticas en Consultas SQL

1. **Consultas Parametrizadas Obligatorias:**
   - Usar siempre el marcador de posición `?` para todos los valores dinámicos.
   - **Nunca concatenar strings ni usar f-strings en sentencias SQL.**
   ```python
   # Correcto:
   cursor.execute("SELECT * FROM users WHERE email = ?;", (email,))

   # Incorrecto:
   cursor.execute(f"SELECT * FROM users WHERE email = '{email}';")
   ```

2. **Confirmación Explícita de Transacciones (`commit`):**
   - Siempre llamar a `conn.commit()` tras ejecutar operaciones de escritura (`INSERT`, `UPDATE`, `DELETE`).
   - Usar el context manager del cursor:
     ```python
     with conn.cursor() as cursor:
         cursor.execute("INSERT INTO items (id, name, price) VALUES (?, ?, ?);", (item_id, name, price))
         conn.commit()
     ```

3. **Manejo de Esquemas y DDL:**
   - Cada repositorio debe incluir un método `init_table()` que ejecute sentencias idempotentes con `CREATE TABLE IF NOT EXISTS`.
   - Los campos de tipo identificador deben definirse como `TEXT PRIMARY KEY` (almacenando UUIDs).
   - Las marcas temporales deben almacenarse como cadenas ISO-8601 UTC (`TEXT NOT NULL`).
   - Los valores booleanos se mapean como enteros (`INTEGER`, 0 o 1).
