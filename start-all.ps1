# FINNOVA - Script de Inicio Completo
$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Iniciando FINNOVA Financial Copilot" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# Paso 1: Verificar Docker
Write-Host "Paso 1: Verificando Docker..." -ForegroundColor Cyan
docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker no esta instalado" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host "OK: Docker instalado" -ForegroundColor Green
Write-Host ""

# Paso 2: Verificar Docker Desktop
Write-Host "Paso 2: Verificando Docker Desktop..." -ForegroundColor Cyan
$dockerOk = $false
for ($i = 1; $i -le 3; $i++) {
    docker ps 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $dockerOk = $true
        break
    }
    
    if ($i -eq 1) {
        Write-Host "Iniciando Docker Desktop..." -ForegroundColor Yellow
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -ErrorAction SilentlyContinue
    }
    
    Write-Host "Esperando Docker Desktop (intento $i/3)..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
}

if (-not $dockerOk) {
    Write-Host "ERROR: Docker Desktop no responde" -ForegroundColor Red
    Write-Host "Inicia Docker Desktop manualmente y vuelve a ejecutar este script" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host "OK: Docker Desktop corriendo" -ForegroundColor Green
Write-Host ""

# Paso 3: PostgreSQL
Write-Host "Paso 3: Configurando PostgreSQL..." -ForegroundColor Cyan
$dbExists = docker ps -a --format "{{.Names}}" | Select-String "financial-copilot-db"

if ($dbExists) {
    $dbRunning = docker ps --format "{{.Names}}" | Select-String "financial-copilot-db"
    if ($dbRunning) {
        Write-Host "OK: PostgreSQL ya esta corriendo" -ForegroundColor Green
    } else {
        Write-Host "Iniciando PostgreSQL..." -ForegroundColor Yellow
        docker start financial-copilot-db | Out-Null
        Start-Sleep -Seconds 8
        Write-Host "OK: PostgreSQL iniciado" -ForegroundColor Green
    }
} else {
    Write-Host "Creando PostgreSQL..." -ForegroundColor Yellow
    docker run -d --name financial-copilot-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=FinancialCopilotDB -p 5432:5432 postgres:15 | Out-Null
    Start-Sleep -Seconds 15
    Write-Host "OK: PostgreSQL creado" -ForegroundColor Green
}
Write-Host ""

# Paso 4: Base de datos
Write-Host "Paso 4: Verificando base de datos..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
docker exec financial-copilot-db psql -U postgres -c "CREATE DATABASE financialcopilot;" 2>&1 | Out-Null
Write-Host "OK: Base de datos lista" -ForegroundColor Green
Write-Host ""

# Paso 5: Migraciones
Write-Host "Paso 5: Aplicando migraciones..." -ForegroundColor Cyan
Push-Location backend/src/FinancialCopilot.API
dotnet ef database update 2>&1 | Out-Null
Pop-Location
Write-Host "OK: Migraciones aplicadas" -ForegroundColor Green
Write-Host ""

# Paso 6: Backend
Write-Host "Paso 6: Iniciando Backend .NET..." -ForegroundColor Cyan
$backendPath = Join-Path $PWD "backend\src\FinancialCopilot.API"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'Backend .NET API' -ForegroundColor Cyan; dotnet run"
Start-Sleep -Seconds 8
Write-Host "OK: Backend en http://localhost:5000" -ForegroundColor Green
Write-Host ""

# Paso 7: AI Engine
Write-Host "Paso 7: Iniciando AI Engine..." -ForegroundColor Cyan
$aiPath = Join-Path $PWD "ai-engine"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$aiPath'; Write-Host 'AI Engine Python' -ForegroundColor Cyan; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 5
Write-Host "OK: AI Engine en http://localhost:8000" -ForegroundColor Green
Write-Host ""

# Paso 8: Frontend
Write-Host "Paso 8: Iniciando Frontend..." -ForegroundColor Cyan
$frontendPath = Join-Path $PWD "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Frontend Next.js' -ForegroundColor Cyan; npm run dev"
Start-Sleep -Seconds 10
Write-Host "OK: Frontend en http://localhost:3000" -ForegroundColor Green
Write-Host ""

# Resumen
Write-Host "============================================" -ForegroundColor Green
Write-Host "FINNOVA esta corriendo!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Servicios:" -ForegroundColor Cyan
Write-Host "  Frontend:    http://localhost:3000" -ForegroundColor White
Write-Host "  Backend API: http://localhost:5000" -ForegroundColor White
Write-Host "  AI Engine:   http://localhost:8000" -ForegroundColor White
Write-Host "  PostgreSQL:  localhost:5432" -ForegroundColor White
Write-Host ""
Write-Host "Abre tu navegador en: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para detener: .\stop-all.ps1" -ForegroundColor Yellow
Write-Host ""

Read-Host "Presiona Enter para cerrar"
