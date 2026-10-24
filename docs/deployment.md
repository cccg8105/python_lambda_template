# Guía de Despliegue Semiautomático Multi-Ambiente

Este documento detalla la estrategia de despliegue para la API serverless en **AWS Lambda** conectada a **Turso**, permitiendo despliegues controlados a entornos aislados (`dev` y `prod`) tanto desde tu terminal local como desde la nube mediante **GitHub Actions**.

---

## 🏛️ Aislamiento por Ambientes (`dev` vs `prod`)

Cada entorno opera de forma completamente independiente a través de stacks dedicados de AWS CloudFormation:

| Parámetro | Ambiente de Desarrollo (`dev`) | Ambiente de Producción (`prod`) |
| :--- | :--- | :--- |
| **Nombre del Stack SAM** | `turso-api-dev` | `turso-api-prod` |
| **Nivel de Log (Powertools)** | `DEBUG` | `INFO` |
| **Secreto en Secrets Manager** | `dev/turso/credentials` | `prod/turso/credentials` |
| **Etiqueta Environment** | `Environment: dev` | `Environment: prod` |
| **URL de API Gateway** | `https://<api-dev-id>.execute-api.<region>.amazonaws.com` | `https://<api-prod-id>.execute-api.<region>.amazonaws.com` |

---

## 🔐 Requisito Previo: Secretos en AWS Secrets Manager

Antes de que la función Lambda pueda conectarse a Turso en AWS, debes crear los secretos correspondientes en tu cuenta de AWS (puedes usar una base de datos de Turso separada para `dev` y otra para `prod`):

1. **Secreto para Dev:** Nombre `dev/turso/credentials`
2. **Secreto para Prod:** Nombre `prod/turso/credentials`
3. **Contenido JSON requerido en el secreto:**
   ```json
   {
     "database_url": "libsql://tu-base-de-datos.turso.io",
     "auth_token": "tu-auth-token-jwt-de-turso"
   }
   ```

---

## 💻 1. Despliegue Local (CLI)

Puedes ejecutar el despliegue semiautomático directamente desde tu terminal de Windows.

### Requisitos locales:
- Tener instalado [AWS CLI](https://aws.amazon.com/cli/) y configurado con tus credenciales (`aws configure`).
- Tener instalado [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

### Comandos de Despliegue:

#### A. Usando el Wrapper de PowerShell (`deploy.ps1`):
```powershell
# Desplegar en el ambiente de desarrollo (dev)
.\deploy.ps1 dev

# Desplegar en el ambiente de producción (prod)
.\deploy.ps1 prod

# Simular el proceso sin aplicar cambios en AWS (Dry-Run)
.\deploy.ps1 dev -DryRun

# Desplegar omitiendo la suite de pruebas (uso excepcional)
.\deploy.ps1 dev -SkipTests
```

#### B. Usando el Script Python Directamente (`scripts/deploy.py`):
```bash
# Despliegue a dev
uv run python scripts/deploy.py --env dev

# Despliegue a prod
uv run python scripts/deploy.py --env prod

# Modo simulación
uv run python scripts/deploy.py --env dev --dry-run
```

### ¿Qué hace el script automáticamente?
1. **Quality Gates:** Ejecuta `uv run ruff check .` y `uv run pytest -v`. Si alguna prueba falla, aborta el despliegue para evitar subir código roto.
2. **Validación SAM:** Ejecuta `sam validate --lint`.
3. **Construcción:** Ejecuta `sam build`.
4. **Despliegue:** Ejecuta `sam deploy --config-env <ambiente>`.

---

## ☁️ 2. Despliegue desde GitHub Actions

GitHub Actions permite disparar el despliegue semiautomático desde la interfaz web de GitHub con un solo clic.

> [!NOTE]
> **Costos de GitHub Actions:**
> - En repositorios públicos: **100% GRATIS e ilimitado**.
> - En repositorios privados: **2,000 minutos gratuitos por mes** (un despliegue de SAM dura aproximadamente 1-2 minutos, lo que permite cientos de despliegues al mes sin costo).

### Paso 1: Configurar Credenciales en GitHub
En tu repositorio de GitHub, dirígete a:  
**Settings > Secrets and variables > Actions > New repository secret**

Agrega los siguientes 3 secretos:
- `AWS_ACCESS_KEY_ID`: Tu Access Key ID de IAM con permisos de CloudFormation, Lambda, API Gateway y Secrets Manager.
- `AWS_SECRET_ACCESS_KEY`: Tu Secret Access Key de IAM.
- `AWS_REGION`: Tu región preferida de AWS (ej. `us-east-1`).

### Paso 2: Disparar el Despliegue Manualmente
1. Ve a la pestaña **Actions** en tu repositorio de GitHub.
2. En la barra lateral izquierda, selecciona el workflow **"Despliegue Semiautomático (AWS SAM)"**.
3. Haz clic en el botón **Run workflow** a la derecha.
4. Selecciona:
   - La rama desde la cual desplegar (habitualmente `main`).
   - El ambiente objetivo (`dev` o `prod`).
5. Haz clic en el botón verde **Run workflow**.

```text
[Run workflow]
  Use workflow from: Branch: main
  Ambiente objetivo de despliegue: [ dev ▼ ]
  Omitir suite de pruebas previas: [ ]
  [Run workflow (Verde)]
```

---

## ⚙️ Configuración Multi-Ambiente en `samconfig.toml`

La configuración de SAM CLI está centralizada en `samconfig.toml`:

```toml
version = 0.1

[default.deploy.parameters]
capabilities = "CAPABILITY_IAM"
confirm_changeset = false
resolve_s3 = true

[dev.deploy.parameters]
stack_name = "turso-api-dev"
parameter_overrides = "Environment=\"dev\" LogLevel=\"DEBUG\" TursoSecretName=\"dev/turso/credentials\""
tags = "Environment=\"dev\" Project=\"python_lambda_template\""

[prod.deploy.parameters]
stack_name = "turso-api-prod"
parameter_overrides = "Environment=\"prod\" LogLevel=\"INFO\" TursoSecretName=\"prod/turso/credentials\""
tags = "Environment=\"prod\" Project=\"python_lambda_template\""
```

El parámetro `resolve_s3 = true` permite que AWS SAM cree y administre automáticamente el bucket de artefactos de despliegue en S3 sin necesidad de configuración manual previa.
