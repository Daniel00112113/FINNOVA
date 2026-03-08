# Script interactivo para preparar la aplicación para producción

Write-Host ""
Write-Host "🚀 PREPARACIÓN PARA PRODUCCIÓN" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$checklist = @(
    @{
        Name = "Generar JWT Key segura"
        Command = ".\generar-claves-seguras.ps1"
        Description = "Genera claves aleatorias seguras"
    },
    @{
        Name = "Configurar appsettings.Production.json"
        File = "backend/src/FinancialCopilot.API/appsettings.Production.json"
        Description = "Actualizar JWT Key, ConnectionString, CORS"
    },
    @{
        Name = "Configurar variables de entorno"
        File = "backend/.env"
        Description = "Copiar .env.example a .env y configurar"
    },
    @{
        Name = "Configurar frontend .env.production"
        File = "frontend/.env.production"
        Description = "Configurar NEXT_PUBLIC_API_URL con dominio real"
    },
    @{
        Name = "Verificar [Authorize] en controllers"
        Description = "Todos los controllers excepto AuthController deben tener [Authorize]"
    },
    @{
        Name = "Probar localmente"
        Command = ".\start-secure.ps1"
        Description = "Iniciar y probar todo el sistema localmente"
    },
    @{
        Name = "Verificar Rate Limiting"
        Description = "Hacer 100+ requests en 1 minuto y verificar error 429"
    },
    @{
        Name = "Verificar HTTPS redirect"
        Description = "En producción, http:// debe redirigir a https://"
    },
    @{
        Name = "Configurar backups automáticos"
        Description = "Script de backup diario de PostgreSQL"
    },
    @{
        Name = "Configurar monitoreo"
        Description = "Application Insights, Sentry, o logs"
    }
)

$completed = 0
$total = $checklist.Count

foreach ($item in $checklist) {
    $num = $checklist.IndexOf($item) + 1
    
    Write-Host ""
    Write-Host "[$num/$total] $($item.Name)" -ForegroundColor Yellow
    Write-Host "     $($item.Description)" -ForegroundColor Gray
    
    if ($item.File) {
        Write-Host "     📁 Archivo: $($item.File)" -ForegroundColor Cyan
    }
    
    if ($item.Command) {
        Write-Host "     💻 Comando: $($item.Command)" -ForegroundColor Cyan
    }
    
    $response = Read-Host "     ¿Completado? (s/n/ejecutar)"
    
    if ($response -eq "ejecutar" -and $item.Command) {
        Write-Host "     Ejecutando..." -ForegroundColor Green
        Invoke-Expression $item.Command
        $completed++
    }
    elseif ($response -eq "s" -or $response -eq "S") {
        Write-Host "     ✅ Marcado como completado" -ForegroundColor Green
        $completed++
    }
    else {
        Write-Host "     ⏭️  Pendiente" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "📊 RESUMEN" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Completados: $completed / $total" -ForegroundColor $(if ($completed -eq $total) { "Green" } else { "Yellow" })

$percentage = [math]::Round(($completed / $total) * 100, 0)
Write-Host "Progreso: $percentage%" -ForegroundColor $(if ($percentage -eq 100) { "Green" } elseif ($percentage -ge 70) { "Yellow" } else { "Red" })

Write-Host ""

if ($completed -eq $total) {
    Write-Host "🎉 ¡TODO LISTO PARA PRODUCCIÓN!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximos pasos:" -ForegroundColor Cyan
    Write-Host "1. Desplegar backend en tu servidor" -ForegroundColor White
    Write-Host "2. Desplegar frontend en Vercel" -ForegroundColor White
    Write-Host "3. Configurar dominio y SSL" -ForegroundColor White
    Write-Host "4. Probar en producción" -ForegroundColor White
}
elseif ($percentage -ge 70) {
    Write-Host "⚠️  Casi listo, completa los items pendientes" -ForegroundColor Yellow
}
else {
    Write-Host "❌ Aún faltan varios items por completar" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
