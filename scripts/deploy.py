#!/usr/bin/env python3
"""Script CLI multiplataforma para despliegue semiautomático con AWS SAM.

Ejecuta validaciones previas de calidad (tests y linter), compila la aplicación
y despliega el stack correspondiente según el ambiente especificado (dev, prod).
"""

import argparse
import subprocess
import sys


def print_banner(message: str) -> None:
    """Imprime un encabezado visual para cada etapa del despliegue."""
    separator = "=" * 70
    print(f"\n{separator}\n>>> {message}\n{separator}")


def run_command(command: list[str], description: str) -> None:
    """Ejecuta un comando en el sistema y detiene la ejecución si falla."""
    print_banner(f"Ejecutando: {description}")
    print(f"Comando: {' '.join(command)}\n")

    result = subprocess.run(command, check=False, shell=(sys.platform == "win32"))
    if result.returncode != 0:
        print(f"\n[ERROR] Falló la etapa: '{description}' (Código de salida: {result.returncode}).")
        print("El despliegue ha sido abortado para proteger la estabilidad del servicio.")
        sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Despliegue semiautomático multi-ambiente para AWS Lambda + Turso."
    )
    parser.add_argument(
        "--env",
        "-e",
        choices=["dev", "staging", "prod"],
        default="dev",
        help="Ambiente objetivo de despliegue (default: dev)",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Omite la ejecución de pytest y ruff antes del despliegue.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compila y valida la plantilla SAM sin aplicar cambios en AWS.",
    )
    args = parser.parse_args()

    print_banner(f"INICIANDO DESPLIEGUE SEMIAUTOMÁTICO: Ambiente '{args.env.upper()}'")

    # 1. Validación de Calidad Previa (Quality Gates)
    if not args.skip_tests:
        run_command(["uv", "run", "ruff", "check", "."], "Verificación de estilo y linting con Ruff")
        run_command(["uv", "run", "pytest", "-v"], "Ejecución de suite de pruebas con Pytest")
    else:
        print("\n[AVISO] Se omitieron las pruebas previas (--skip-tests).")

    # 2. Validación de la Plantilla SAM
    run_command(["sam", "validate", "--lint"], "Validación de la plantilla AWS SAM (template.yaml)")

    # 3. Preparación de dependencias de producción
    run_command(
        ["uv", "export", "--no-dev", "--no-hashes", "-o", "src/requirements.txt"],
        "Generación de dependencias de producción (uv export)",
    )

    # 4. Compilación de la Aplicación Serverless
    run_command(["sam", "build"], "Construcción de artefactos serverless (sam build)")

    # 4. Despliegue en AWS
    if args.dry_run:
        print_banner("MODO DRY-RUN COMPLETADO")
        print(f"La aplicación compiló correctamente para el ambiente '{args.env}'.")
        print("No se realizaron cambios en la cuenta de AWS.")
        return

    deploy_cmd = ["sam", "deploy", "--config-env", args.env]
    run_command(deploy_cmd, f"Despliegue del stack en AWS (Ambiente: {args.env})")

    print_banner(f"DESPLIEGUE FINALIZADO CON ÉXITO: '{args.env.upper()}'")
    print("Recursos desplegados y configurados correctamente en AWS.")
    print(f"Stack correspondiente: 'turso-api-{args.env}'")


if __name__ == "__main__":
    main()
