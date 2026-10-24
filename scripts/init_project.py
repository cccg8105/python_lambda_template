#!/usr/bin/env python3
"""Script de inicialización y personalización para python_lambda_template.

Permite configurar un nuevo proyecto a partir de la plantilla:
- Renombra el paquete y descripción en pyproject.toml
- Actualiza nombres de servicio en código y pruebas
- Configura nombres de stack y tags en AWS SAM (template.yaml y samconfig.toml)
- Reinicia el CHANGELOG.md y actualiza README.md
- Limpia requerimientos de ejemplo en el backlog
- Opcionalmente reinicia el repositorio Git con un commit inicial limpio
- Sincroniza uv, regenera locks y valida calidad (Ruff y Pytest)
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


def print_banner(message: str) -> None:
    separator = "=" * 70
    print(f"\n{separator}\n>>> {message}\n{separator}")


def to_kebab_case(text: str) -> str:
    """Convierte texto a kebab-case (ej. 'Mi Nuevo Servicio' -> 'mi-nuevo-servicio')."""
    clean = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s_]+", "-", clean)


def to_snake_case(text: str) -> str:
    """Convierte texto a snake_case (ej. 'mi-nuevo-servicio' -> 'mi_nuevo_servicio')."""
    return to_kebab_case(text).replace("-", "_")


def to_title_case(text: str) -> str:
    """Convierte texto a Title Case legible (ej. 'mi-nuevo-servicio' -> 'Mi Nuevo Servicio')."""
    words = re.sub(r"[-_]+", " ", text).split()
    return " ".join(word.capitalize() for word in words)


def run_command(command: list[str], description: str) -> None:
    """Ejecuta un comando del sistema y aborta si hay error."""
    print_banner(f"Ejecutando: {description}")
    print(f"Comando: {' '.join(command)}\n")

    result = subprocess.run(command, check=False, shell=(sys.platform == "win32"))
    if result.returncode != 0:
        print(f"\n[ERROR] Falló la etapa: '{description}' (Código: {result.returncode}).")
        sys.exit(result.returncode)


def replace_in_file(path: Path, replacements: list[tuple[str, str]], dry_run: bool) -> None:
    """Aplica reemplazos literales en un archivo."""
    if not path.exists():
        print(f"[AVISO] Archivo no encontrado: {path}")
        return

    content = path.read_text(encoding="utf-8")
    original_content = content

    for target, replacement in replacements:
        content = content.replace(target, replacement)

    if content != original_content:
        if dry_run:
            print(f"[DRY-RUN] Modificaría: {path.name}")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"[OK] Actualizado: {path.name}")


def clean_backlog_samples(root_dir: Path, dry_run: bool) -> None:
    """Elimina requerimientos de ejemplo y limpia las tablas de READMEs en backlog."""
    sample_files = [
        root_dir / "backlog" / "completed" / "FEAT-000-plantilla-base.md",
        root_dir / "backlog" / "pending" / "FEAT-001-usuarios-crud.md",
    ]

    for file_path in sample_files:
        if file_path.exists():
            if dry_run:
                print(f"[DRY-RUN] Eliminaría ejemplo de backlog: {file_path.name}")
            else:
                file_path.unlink()
                print(f"[OK] Eliminado ejemplo de backlog: {file_path.name}")

    # Limpiar tabla en backlog/pending/README.md
    pending_readme = root_dir / "backlog" / "pending" / "README.md"
    if pending_readme.exists():
        new_pending_content = """# Requerimientos Pendientes

Listado de especificaciones de features planificados para desarrollo.

| ID | Título | Versión Objetivo | Estado | Archivo de Especificación |
| :--- | :--- | :--- | :--- | :--- |
| - | *(No hay requerimientos pendientes)* | - | - | - |
"""
        if dry_run:
            print(f"[DRY-RUN] Reiniciaría tabla en: {pending_readme.relative_to(root_dir)}")
        else:
            pending_readme.write_text(new_pending_content, encoding="utf-8")
            print(f"[OK] Reiniciado: {pending_readme.relative_to(root_dir)}")

    # Limpiar tabla en backlog/completed/README.md
    completed_readme = root_dir / "backlog" / "completed" / "README.md"
    if completed_readme.exists():
        new_completed_content = """# Requerimientos Completados

Historial de especificaciones de requerimientos desarrollados y verificados.

| ID | Título | Versión Lanzada | Fecha de Finalización | Archivo de Especificación |
| :--- | :--- | :--- | :--- | :--- |
| - | *(Aún no hay requerimientos completados)* | - | - | - |
"""
        if dry_run:
            print(f"[DRY-RUN] Reiniciaría tabla en: {completed_readme.relative_to(root_dir)}")
        else:
            completed_readme.write_text(new_completed_content, encoding="utf-8")
            print(f"[OK] Reiniciado: {completed_readme.relative_to(root_dir)}")


def reset_changelog(root_dir: Path, project_title: str, dry_run: bool) -> None:
    """Reinicia CHANGELOG.md para el nuevo proyecto."""
    changelog_path = root_dir / "CHANGELOG.md"
    today_str = datetime.now(UTC).strftime("%Y-%m-%d")

    content = f"""# Changelog - {project_title}

Todos los cambios notables de este proyecto serán documentados en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - {today_str}
### Added
- Inicialización del proyecto a partir de la plantilla serverless desacoplada.
- Arquitectura limpia con soporte para AWS Lambda, API Gateway HTTP API v2 y Turso.
- Suite de pruebas automatizadas y quality gates con Ruff y Pytest.
- Despliegue semiautomático multiente (dev/prod) con AWS SAM.
"""
    if dry_run:
        print(f"[DRY-RUN] Reiniciaría: {changelog_path.name}")
    else:
        changelog_path.write_text(content, encoding="utf-8")
        print(f"[OK] Reiniciado: {changelog_path.name}")


def reset_git_repository(root_dir: Path, project_slug: str, dry_run: bool) -> None:
    """Elimina el historial de git existente e inicializa un repositorio nuevo y limpio."""
    git_dir = root_dir / ".git"
    if git_dir.exists():
        if dry_run:
            print("[DRY-RUN] Eliminaría carpeta .git/ e inicializaría un nuevo repositorio Git.")
            return

        print_banner("Reiniciando repositorio Git")
        # Eliminar carpeta .git
        shutil.rmtree(git_dir, ignore_errors=True)
        print("[OK] Historial previo de Git eliminado.")

        # Re-inicializar git
        run_command(["git", "init", "-b", "main"], "Inicialización de nuevo repositorio Git")
        run_command(["git", "add", "."], "Indexación de archivos del nuevo proyecto")
        run_command(
            ["git", "commit", "-m", f"feat: initial commit for {project_slug}"],
            "Creación de commit inicial",
        )
        print(f"[OK] Repositorio Git reinicializado en la rama 'main' para '{project_slug}'.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inicializa y personaliza un nuevo proyecto a partir de python_lambda_template."
    )
    parser.add_argument(
        "--name",
        "-n",
        help="Nombre del nuevo proyecto/servicio (ej. order-service o 'Order Service').",
    )
    parser.add_argument(
        "--description",
        "-d",
        help="Breve descripción del servicio o API.",
    )
    parser.add_argument(
        "--reset-git",
        action="store_true",
        help="Reinicia el historial de Git (elimina .git/ y crea un commit inicial limpio en main).",
    )
    parser.add_argument(
        "--clean-backlog",
        action="store_true",
        default=True,
        help="Limpia requerimientos de ejemplo en backlog/ (default: True).",
    )
    parser.add_argument(
        "--keep-script",
        action="store_true",
        help="Conserva scripts/init_project.py tras finalizar sin preguntar por su eliminación.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula todas las operaciones sin modificar archivos ni reiniciar Git.",
    )

    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parent.parent

    # Modo interactivo si no se proporcionó nombre
    project_name = args.name
    if not project_name:
        if sys.stdin.isatty():
            print_banner("INICIALIZACIÓN DE NUEVO PROYECTO")
            try:
                project_name = input(
                    "Nombre del nuevo proyecto/servicio [ej. order-service]: "
                ).strip()
            except (KeyboardInterrupt, EOFError):
                print("\nOperación cancelada por el usuario.")
                sys.exit(1)
        if not project_name:
            print("[ERROR] Debes especificar un nombre de proyecto mediante --name o en consola.")
            sys.exit(1)

    project_slug = to_kebab_case(project_name)
    project_snake = to_snake_case(project_name)
    project_title = to_title_case(project_name)

    project_desc = args.description
    if not project_desc:
        if sys.stdin.isatty() and not args.name:
            try:
                project_desc = input(
                    f"Descripción del servicio [{project_title} API]: "
                ).strip()
            except (KeyboardInterrupt, EOFError):
                project_desc = ""
        if not project_desc:
            project_desc = f"{project_title} API Serverless"

    reset_git = args.reset_git
    if not reset_git and not args.dry_run and sys.stdin.isatty() and not args.name:
        try:
            confirm_git = input(
                "¿Deseas reiniciar el repositorio Git con un historial limpio? (s/N): "
            ).strip().lower()
            reset_git = confirm_git in ["s", "si", "y", "yes"]
        except (KeyboardInterrupt, EOFError):
            reset_git = False

    print_banner(f"CONFIGURANDO: '{project_title}' ({project_slug})")
    print(f"Directorio raíz: {root_dir}")
    print(f"Identificador kebab-case: {project_slug}")
    print(f"Identificador snake_case: {project_snake}")
    print(f"Descripción:             {project_desc}")
    print(f"Reiniciar Git:           {'Sí' if reset_git else 'No'}")
    print(f"Modo Dry-Run:            {'Activo' if args.dry_run else 'Inactivo'}")

    # 1. pyproject.toml
    replace_in_file(
        root_dir / "pyproject.toml",
        [
            ('name = "python-lambda-turso-template"', f'name = "{project_slug}"'),
            (
                'description = "Plantilla desacoplada para AWS Lambda con API Gateway HTTP API y Turso Serverless"',
                f'description = "{project_desc}"',
            ),
        ],
        args.dry_run,
    )

    # 2. samconfig.toml
    replace_in_file(
        root_dir / "samconfig.toml",
        [
            ('stack_name = "turso-api-dev"', f'stack_name = "{project_slug}-dev"'),
            ('stack_name = "turso-api-prod"', f'stack_name = "{project_slug}-prod"'),
            ('Project=\\"python_lambda_template\\"', f'Project=\\"{project_snake}\\"'),
        ],
        args.dry_run,
    )

    # 3. template.yaml
    replace_in_file(
        root_dir / "template.yaml",
        [
            (
                'POWERTOOLS_SERVICE_NAME: !Sub "turso-api-${Environment}"',
                f'POWERTOOLS_SERVICE_NAME: !Sub "{project_slug}-${{Environment}}"',
            ),
            ('Project: python_lambda_template', f'Project: {project_snake}'),
            (
                'Description: !Sub "API Serverless conectada a Turso (${Environment})"',
                f'Description: !Sub "{project_desc} (${{Environment}})"',
            ),
        ],
        args.dry_run,
    )

    # 4. Código fuente
    replace_in_file(
        root_dir / "src" / "app" / "main.py",
        [('service="turso-api-service"', f'service="{project_slug}-service"')],
        args.dry_run,
    )
    replace_in_file(
        root_dir / "src" / "app" / "api" / "routes" / "health.py",
        [('"service": "turso-api-service"', f'"service": "{project_slug}-service"')],
        args.dry_run,
    )

    # 5. Pruebas
    replace_in_file(
        root_dir / "tests" / "integration" / "test_routes.py",
        [('assert body["service"] == "turso-api-service"', f'assert body["service"] == "{project_slug}-service"')],
        args.dry_run,
    )
    replace_in_file(
        root_dir / "tests" / "conftest.py",
        [
            ('function_name: str = "turso-api-function"', f'function_name: str = "{project_slug}-function"'),
            (
                'invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:turso-api"',
                f'invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:{project_slug}"',
            ),
        ],
        args.dry_run,
    )

    # 6. README.md
    replace_in_file(
        root_dir / "README.md",
        [
            (
                "# AWS Lambda + API Gateway v2 + Turso Serverless (Clean Architecture)",
                f"# {project_title} (Serverless API)",
            ),
            (".\\deploy.ps1 dev     # Despliega a turso-api-dev", f".\\deploy.ps1 dev     # Despliega a {project_slug}-dev"),
            (".\\deploy.ps1 prod    # Despliega a turso-api-prod", f".\\deploy.ps1 prod    # Despliega a {project_slug}-prod"),
        ],
        args.dry_run,
    )

    # 7. scripts/deploy.py
    replace_in_file(
        root_dir / "scripts" / "deploy.py",
        [
            ("Stack correspondiente: 'turso-api-{args.env}'", f"Stack correspondiente: '{project_slug}-{{args.env}}'"),
        ],
        args.dry_run,
    )

    # 8. Reiniciar CHANGELOG.md
    reset_changelog(root_dir, project_title, args.dry_run)

    # 9. Limpiar ejemplos del backlog
    if args.clean_backlog:
        clean_backlog_samples(root_dir, args.dry_run)

    # Si es dry-run, terminamos aquí sin tocar Git ni dependencias
    if args.dry_run:
        print_banner("MODO SIMULACIÓN (DRY-RUN) COMPLETADO CON ÉXITO")
        print("Todas las sustituciones de archivos fueron verificadas correctamente.")
        return

    # 10. Sincronización de dependencias y regeneración de locks con uv
    run_command(["uv", "lock"], "Actualización de lockfile (uv lock)")
    run_command(["uv", "sync"], "Sincronización del entorno virtual (uv sync)")
    run_command(
        ["uv", "export", "--no-dev", "--no-hashes", "-o", "src/requirements.txt"],
        "Generación de dependencias de producción para SAM (uv export)",
    )

    # 11. Quality Gates (Ruff y Pytest)
    run_command(["uv", "run", "ruff", "check", "--fix", "."], "Verificación y formateo con Ruff")
    run_command(["uv", "run", "pytest", "-v"], "Ejecución de suite de pruebas con Pytest")

    # 12. Reinicio de Git si fue solicitado
    if reset_git:
        reset_git_repository(root_dir, project_slug, args.dry_run)

    print_banner(f"PROYECTO '{project_title}' INICIALIZADO CON ÉXITO")
    print(f"Todo está listo y verificado para comenzar el desarrollo de '{project_slug}'.")

    # 13. Opcional: auto-eliminación del script de inicialización
    if not args.keep_script:
        should_delete = False
        if sys.stdin.isatty():
            try:
                resp = input(
                    "\n¿Deseas eliminar el script 'scripts/init_project.py' para limpiar el proyecto? (s/N): "
                ).strip().lower()
                should_delete = resp in ["s", "si", "y", "yes"]
            except (KeyboardInterrupt, EOFError):
                should_delete = False

        if should_delete:
            script_path = Path(__file__).resolve()
            script_path.unlink()
            print("[OK] Script 'scripts/init_project.py' eliminado satisfactoriamente.")


if __name__ == "__main__":
    main()
