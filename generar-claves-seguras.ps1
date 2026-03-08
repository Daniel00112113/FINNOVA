# Script para generar claves seguras para producción

Write-Host "🔐 GENERADOR DE CLAVES SEGURAS" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Generar JWT Key (64 caracteres)
Write-Host "1️⃣  JWT Key (64 caracteres):" -ForegroundColor Yellow
$jwtKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})
Write-Host $jwtKey -ForegroundColor Green
Write-Host ""

# Generar Database Password (32 caracteres)
Write-Host "2️⃣  Database Password (32 caracteres):" -ForegroundColor Yellow
$dbPassword = -join ((65..90) + (97..122) + (48..57) + 33,35,36,37,38,42,43,45,61,63,64 | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host $dbPassword -ForegroundColor Green
Write-Host ""

# Generar API Key (opcional, 32 caracteres)
Write-Host "3️⃣  API Key (opcional, 32 caracteres):" -ForegroundColor Yellow
$apiKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host $apiKey -ForegroundColor Green
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Claves generadas exitosamente" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Red
Write-Host "   - Guarda estas claves en un lugar seguro" -ForegroundColor Yellow
Write-Host "   - NO las subas a Git" -ForegroundColor Yellow
Write-Host "   - Úsalas en tus archivos .env o appsettings.Production.json" -ForegroundColor Yellow
Write-Host ""

# Preguntar si quiere guardar en archivo
$save = Read-Host "¿Guardar claves en archivo 'claves-generadas.txt'? (s/n)"
if ($save -eq "s" -or $save -eq "S") {
    $content = @"
CLAVES GENERADAS - $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
================================================================

JWT_KEY=$jwtKey

DATABASE_PASSWORD=$dbPassword

API_KEY=$apiKey

================================================================
⚠️ IMPORTANTE: Elimina este archivo después de copiar las claves
================================================================
"@
    
    $content | Out-File -FilePath "claves-generadas.txt" -Encoding UTF8
    Write-Host "✅ Claves guardadas en 'claves-generadas.txt'" -ForegroundColor Green
    Write-Host "⚠️  Recuerda eliminar este archivo después de usarlo" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
