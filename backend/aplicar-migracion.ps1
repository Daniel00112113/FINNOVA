# Script para aplicar migración de campos extendidos
# Ejecutar desde la carpeta backend

Write-Host "=== Aplicando Migración de Campos Extendidos ===" -ForegroundColor Green

# Configuración de PostgreSQL
$env:PGPASSWORD = "postgres"  # Cambia esto si tu contraseña es diferente
$dbName = "FinancialCopilot"
$dbUser = "postgres"
$dbHost = "localhost"
$dbPort = "5432"

# SQL a ejecutar
$sql = @"
-- Agregar columna Location
ALTER TABLE "Expenses" 
ADD COLUMN IF NOT EXISTS "Location" VARCHAR(200);

-- Agregar columna IsRecurring
ALTER TABLE "Expenses" 
ADD COLUMN IF NOT EXISTS "IsRecurring" BOOLEAN DEFAULT FALSE;

-- Agregar columna RecurrenceType
ALTER TABLE "Expenses" 
ADD COLUMN IF NOT EXISTS "RecurrenceType" VARCHAR(50);

-- Agregar columna Tags
ALTER TABLE "Expenses" 
ADD COLUMN IF NOT EXISTS "Tags" TEXT;

-- Comentarios
COMMENT ON COLUMN "Expenses"."Location" IS 'Ubicación opcional del gasto';
COMMENT ON COLUMN "Expenses"."IsRecurring" IS 'Indica si el gasto es recurrente';
COMMENT ON COLUMN "Expenses"."RecurrenceType" IS 'Tipo de recurrencia: Daily, Weekly, Monthly, Yearly';
COMMENT ON COLUMN "Expenses"."Tags" IS 'Etiquetas personalizadas separadas por comas';

-- Verificar columnas
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'Expenses'
ORDER BY ordinal_position;
"@

# Guardar SQL en archivo temporal
$tempFile = [System.IO.Path]::GetTempFileName() + ".sql"
$sql | Out-File -FilePath $tempFile -Encoding UTF8

Write-Host "Ejecutando migración..." -ForegroundColor Yellow

try {
    # Intentar ejecutar con psql
    $psqlPath = "psql"
    
    # Verificar si psql está en el PATH
    $psqlExists = Get-Command psql -ErrorAction SilentlyContinue
    
    if (-not $psqlExists) {
        # Buscar psql en ubicaciones comunes
        $possiblePaths = @(
            "C:\Program Files\PostgreSQL\16\bin\psql.exe",
            "C:\Program Files\PostgreSQL\15\bin\psql.exe",
            "C:\Program Files\PostgreSQL\14\bin\psql.exe",
            "C:\Program Files (x86)\PostgreSQL\16\bin\psql.exe"
        )
        
        foreach ($path in $possiblePaths) {
            if (Test-Path $path) {
                $psqlPath = $path
                break
            }
        }
    }
    
    # Ejecutar psql
    & $psqlPath -h $dbHost -p $dbPort -U $dbUser -d $dbName -f $tempFile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Migración aplicada exitosamente!" -ForegroundColor Green
        Write-Host "`nAhora puedes:" -ForegroundColor Cyan
        Write-Host "1. Recargar la página de análisis" -ForegroundColor White
        Write-Host "2. Probar el formulario de gastos con los nuevos campos" -ForegroundColor White
    } else {
        Write-Host "`n✗ Error al aplicar migración" -ForegroundColor Red
        Write-Host "Código de salida: $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "`n✗ Error: $_" -ForegroundColor Red
    Write-Host "`nNo se pudo encontrar psql. Por favor:" -ForegroundColor Yellow
    Write-Host "1. Abre pgAdmin" -ForegroundColor White
    Write-Host "2. Conecta a la base de datos 'FinancialCopilot'" -ForegroundColor White
    Write-Host "3. Abre Query Tool" -ForegroundColor White
    Write-Host "4. Copia y pega el contenido de: backend/MIGRACION_CAMPOS_EXPENSE.sql" -ForegroundColor White
    Write-Host "5. Ejecuta (F5)" -ForegroundColor White
} finally {
    # Limpiar archivo temporal
    if (Test-Path $tempFile) {
        Remove-Item $tempFile
    }
}

# Limpiar variable de entorno
Remove-Item Env:\PGPASSWORD
