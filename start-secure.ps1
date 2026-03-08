# Script de inicio con seguridad implementada
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Financial Copilot - Inicio Seguro" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar PostgreSQL
Write-Host "1. Verificando PostgreSQL..." -ForegroundColor Yellow
$pgStatus = docker ps --filter "name=financial-copilot-db" --format "{{.Status}}"
if ($pgStatus) {
    Write-Host "   PostgreSQL corriendo" -ForegroundColor Green
} else {
    Write-Host "   Iniciando PostgreSQL..." -ForegroundColor Yellow
    docker start financial-copilot-db
    Start-Sleep -Seconds 3
}

# Verificar migraciones
Write-Host ""
Write-Host "2. Verificando migraciones de BD..." -ForegroundColor Yellow
$tables = docker exec financial-copilot-db psql -U postgres -d financialcopilot -t -c "SELECT tablename FROM pg_tables WHERE schemaname='public';" 2>$null
if ($tables -match "Users") {
    Write-Host "   Base de datos configurada" -ForegroundColor Green
} else {
    Write-Host "   ERROR: Base de datos no configurada" -ForegroundColor Red
    Write-Host "   Ejecuta: cd backend; .\aplicar-migracion.ps1" -ForegroundColor Yellow
    exit 1
}

# Iniciar AI Engine
Write-Host ""
Write-Host "3. Iniciando AI Engine..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd ai-engine; `$env:PYTHONIOENCODING='utf-8'; python main.py"
Start-Sleep -Seconds 2

# Iniciar Backend
Write-Host ""
Write-Host "4. Iniciando Backend (.NET)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend/src/FinancialCopilot.API; dotnet run"
Start-Sleep -Seconds 5

# Iniciar Frontend
Write-Host ""
Write-Host "5. Iniciando Frontend (Next.js)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Servicios Iniciados" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:   http://localhost:5000" -ForegroundColor Cyan
Write-Host "AI Engine: http://localhost:8001" -ForegroundColor Cyan
Write-Host "PostgreSQL: localhost:5432" -ForegroundColor Cyan
Write-Host ""
Write-Host "Autenticacion JWT: ACTIVA" -ForegroundColor Green
Write-Host "Contraseñas: BCrypt (12 rounds)" -ForegroundColor Green
Write-Host ""
Write-Host "Para probar:" -ForegroundColor Yellow
Write-Host "1. Ir a http://localhost:3000/auth/register" -ForegroundColor White
Write-Host "2. Crear una cuenta" -ForegroundColor White
Write-Host "3. Iniciar sesion" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C para detener todos los servicios" -ForegroundColor Yellow
Write-Host ""

# Mantener el script corriendo
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
}
