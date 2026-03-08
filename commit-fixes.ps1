# Script para hacer commit de las correcciones de .NET 8

Write-Host "🔧 Preparando commit de correcciones..." -ForegroundColor Cyan

# Verificar estado de git
Write-Host "`n📋 Estado actual de Git:" -ForegroundColor Yellow
git status

# Agregar archivos modificados
Write-Host "`n➕ Agregando archivos modificados..." -ForegroundColor Cyan
git add backend/Dockerfile
git add backend/src/FinancialCopilot.API/FinancialCopilot.API.csproj
git add backend/src/FinancialCopilot.Application/FinancialCopilot.Application.csproj
git add backend/src/FinancialCopilot.Domain/FinancialCopilot.Domain.csproj
git add backend/src/FinancialCopilot.Infrastructure/FinancialCopilot.Infrastructure.csproj
git add SOLUCION_ERRORES_RENDER.md
git add RENDER_CONFIGURACION_ACTUAL.md
git add commit-fixes.ps1

# Mostrar archivos que se van a commitear
Write-Host "`n📝 Archivos a commitear:" -ForegroundColor Yellow
git status --short

# Hacer commit
Write-Host "`n💾 Haciendo commit..." -ForegroundColor Cyan
git commit -m "fix: Cambiar de .NET 10 a .NET 8 para compatibilidad con Render

- Actualizar todos los .csproj de net10.0 a net8.0
- Actualizar Dockerfile para usar .NET SDK 8.0
- Ajustar versiones de paquetes NuGet para .NET 8
- Agregar documentación de solución de errores
- Actualizar guía de configuración de Render"

# Verificar que el commit se hizo correctamente
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Commit realizado exitosamente!" -ForegroundColor Green
    
    # Preguntar si quiere hacer push
    Write-Host "`n¿Deseas hacer push a GitHub ahora? (S/N): " -ForegroundColor Yellow -NoNewline
    $respuesta = Read-Host
    
    if ($respuesta -eq "S" -or $respuesta -eq "s") {
        Write-Host "`n🚀 Haciendo push a GitHub..." -ForegroundColor Cyan
        git push origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Push realizado exitosamente!" -ForegroundColor Green
            Write-Host "`n📋 Próximos pasos:" -ForegroundColor Cyan
            Write-Host "1. Ve a Render Dashboard" -ForegroundColor White
            Write-Host "2. Los servicios se redesplegarán automáticamente" -ForegroundColor White
            Write-Host "3. O haz 'Manual Deploy' en cada servicio" -ForegroundColor White
            Write-Host "4. Verifica los logs para confirmar que todo funciona" -ForegroundColor White
        } else {
            Write-Host "`n❌ Error al hacer push. Verifica tu conexión y permisos." -ForegroundColor Red
        }
    } else {
        Write-Host "`n⏸️  Push cancelado. Puedes hacerlo manualmente con:" -ForegroundColor Yellow
        Write-Host "   git push origin main" -ForegroundColor White
    }
} else {
    Write-Host "`n❌ Error al hacer commit. Revisa los mensajes de error arriba." -ForegroundColor Red
}

Write-Host "`n✨ Script completado." -ForegroundColor Cyan
