# Script para verificar estado del AI Engine
Write-Host "Verificando estado del AI Engine..." -ForegroundColor Cyan
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8001/" -Method Get
    
    Write-Host "AI Engine esta corriendo" -ForegroundColor Green
    Write-Host ""
    Write-Host "Estado:" -ForegroundColor Yellow
    Write-Host "  - Mensaje: $($response.message)"
    Write-Host "  - Estado: $($response.status)"
    Write-Host "  - Modelo Profesional: $($response.professional_ai)"
    Write-Host "  - Advanced AI: $($response.advanced_ai)"
    Write-Host "  - Smart AI: $($response.smart_ai)"
    Write-Host "  - Modelo: $($response.model)"
    Write-Host ""
    
    if ($response.professional_ai -eq $true) {
        Write-Host "Modelo Profesional ACTIVO y funcionando" -ForegroundColor Green
    } else {
        Write-Host "Modelo Profesional no disponible" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "AI Engine no esta corriendo" -ForegroundColor Red
    Write-Host ""
    Write-Host "Para iniciar el AI Engine:" -ForegroundColor Yellow
    Write-Host "  cd ai-engine"
    Write-Host "  python main.py"
    Write-Host ""
}
