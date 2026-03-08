# Stop Simple - Detiene todos los servicios
Write-Host "Deteniendo servicios..." -ForegroundColor Yellow

# Detener procesos de PowerShell (Backend, Frontend, AI Engine)
Write-Host "Deteniendo procesos..." -ForegroundColor Gray
Get-Process powershell | Where-Object { $_.MainWindowTitle -match "dotnet|npm|python" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Detener PostgreSQL (opcional - comentado para mantener datos)
# Write-Host "Deteniendo PostgreSQL..." -ForegroundColor Gray
# docker stop financial-copilot-db

Write-Host "Servicios detenidos" -ForegroundColor Green
