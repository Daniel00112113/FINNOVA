# Aplicar Migración de Campos Extendidos

## Opción 1: Usando psql (Recomendado)

1. Abre una terminal
2. Ejecuta:
```bash
psql -U postgres -d FinancialCopilot -f backend/MIGRACION_CAMPOS_EXPENSE.sql
```

Si no tienes psql en el PATH, usa la ruta completa:
```bash
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d FinancialCopilot -f backend/MIGRACION_CAMPOS_EXPENSE.sql
```

## Opción 2: Usando pgAdmin

1. Abre pgAdmin
2. Conecta a tu servidor PostgreSQL
3. Selecciona la base de datos "FinancialCopilot"
4. Click derecho → Query Tool
5. Copia y pega el contenido de `backend/MIGRACION_CAMPOS_EXPENSE.sql`
6. Click en Execute (F5)

## Opción 3: Ejecutar SQL directamente

Copia y pega esto en tu herramienta de PostgreSQL:

```sql
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
```

## Verificar que funcionó

Ejecuta esto para verificar:
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'Expenses';
```

Deberías ver las nuevas columnas: Location, IsRecurring, RecurrenceType, Tags

## Después de aplicar la migración

1. El backend debería funcionar automáticamente
2. Recarga la página de análisis
3. El error 500 debería desaparecer
