<#
.SYNOPSIS
    Script de conveniencia en PowerShell para despliegue semiautomático en Windows.
.EXAMPLE
    .\deploy.ps1 dev
    .\deploy.ps1 prod
    .\deploy.ps1 dev -DryRun
    .\deploy.ps1 dev -SkipTests
#>
param(
    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment = "dev",

    [switch]$SkipTests,
    [switch]$DryRun
)

$argsList = @("scripts/deploy.py", "--env", $Environment)

if ($SkipTests) {
    $argsList += "--skip-tests"
}

if ($DryRun) {
    $argsList += "--dry-run"
}

Write-Host "Iniciando despliegue para ambiente: $Environment" -ForegroundColor Cyan
uv run python @argsList
