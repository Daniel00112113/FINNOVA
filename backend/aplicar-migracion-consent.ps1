# Script para aplicar migración de UserConsent
# Usa docker exec para ejecutar SQL sin necesidad de psql instalado

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Aplicando Migración: UserConsent" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Docker esté corriendo
Write-Host "Verificando Docker..." -ForegroundColor Yellow
docker ps | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker no está corriendo" -ForegroundColor Red
    Write-Host "Inicia Docker Desktop y vuelve a intentar" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que el contenedor de PostgreSQL exista
Write-Host "Verificando contenedor de PostgreSQL..." -ForegroundColor Yellow
$container = docker ps -a --format "{{.Names}}" | Select-String "financial-copilot-db"

if (-not $container) {
    Write-Host "ERROR: Contenedor 'financial-copilot-db' no encontrado" -ForegroundColor Red
    Write-Host "Ejecuta start-all.ps1 primero para crear el contenedor" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que el contenedor esté corriendo
$running = docker ps --format "{{.Names}}" | Select-String "financial-copilot-db"
if (-not $running) {
    Write-Host "Iniciando contenedor de PostgreSQL..." -ForegroundColor Yellow
    docker start financial-copilot-db | Out-Null
    Start-Sleep -Seconds 5
}

Write-Host "OK: PostgreSQL listo" -ForegroundColor Green
Write-Host ""

# Aplicar migración
Write-Host "Aplicando migración..." -ForegroundColor Cyan
Write-Host ""

# Copiar archivo SQL al contenedor
docker cp MIGRACION_USER_CONSENT.sql financial-copilot-db:/tmp/migration.sql

# Ejecutar SQL
$result = docker exec financial-copilot-db psql -U postgres -d FinancialCopilotDB -f /tmp/migration.sql 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "✅ MIGRACIÓN APLICADA EXITOSAMENTE" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tabla UserConsent creada correctamente" -ForegroundColor Green
    Write-Host ""
    
    # Mostrar estadísticas
    Write-Host "Estadísticas:" -ForegroundColor Cyan
    docker exec financial-copilot-db psql -U postgres -d FinancialCopilotDB -c 'SELECT COUNT(*) as total_users FROM "UserConsent";'
    
} else {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Red
    Write-Host "❌ ERROR AL APLICAR MIGRACIÓN" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Detalles del error:" -ForegroundColor Yellow
    Write-Host $result
    Write-Host ""
}

Write-Host ""
Read-Host "Presiona Enter para continuar"
