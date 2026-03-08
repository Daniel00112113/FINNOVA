# Script para aplicar migración de campos de Expense
Write-Host "Aplicando migracion de campos de Expense..." -ForegroundColor Cyan
Write-Host ""

# Configuración
$containerName = "financial-copilot-db"
$database = "financialcopilot"
$sqlFile = "MIGRACION_CAMPOS_EXPENSE.sql"

# Verificar que el contenedor esté corriendo
Write-Host "Verificando contenedor PostgreSQL..." -ForegroundColor Yellow
$containerStatus = docker ps --filter "name=$containerName" --format "{{.Status}}"

if (-not $containerStatus) {
    Write-Host "ERROR: El contenedor $containerName no esta corriendo" -ForegroundColor Red
    Write-Host "Inicia el contenedor con: docker start $containerName" -ForegroundColor Yellow
    exit 1
}

Write-Host "Contenedor activo: $containerStatus" -ForegroundColor Green
Write-Host ""

# Aplicar migración
Write-Host "Aplicando migracion desde $sqlFile..." -ForegroundColor Yellow
Write-Host ""

docker exec -i $containerName psql -U postgres -d $database -f /tmp/migration.sql < $sqlFile

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Migracion aplicada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Verificando estructura de tabla Expenses..." -ForegroundColor Yellow
    docker exec $containerName psql -U postgres -d $database -c "\d `"Expenses`""
} else {
    Write-Host ""
    Write-Host "ERROR: Fallo al aplicar la migracion" -ForegroundColor Red
    exit 1
}
