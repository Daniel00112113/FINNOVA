-- Migración: Agregar campos faltantes a tabla Expenses
-- Fecha: 2026-03-07
-- Descripción: Agrega Location, IsRecurring, RecurrenceType y Tags

-- Verificar si las columnas ya existen antes de agregarlas
DO $$ 
BEGIN
    -- Agregar columna Location
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'Expenses' AND column_name = 'Location'
    ) THEN
        ALTER TABLE "Expenses" ADD COLUMN "Location" TEXT NULL;
        RAISE NOTICE 'Columna Location agregada';
    ELSE
        RAISE NOTICE 'Columna Location ya existe';
    END IF;

    -- Agregar columna IsRecurring
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'Expenses' AND column_name = 'IsRecurring'
    ) THEN
        ALTER TABLE "Expenses" ADD COLUMN "IsRecurring" BOOLEAN NOT NULL DEFAULT FALSE;
        RAISE NOTICE 'Columna IsRecurring agregada';
    ELSE
        RAISE NOTICE 'Columna IsRecurring ya existe';
    END IF;

    -- Agregar columna RecurrenceType
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'Expenses' AND column_name = 'RecurrenceType'
    ) THEN
        ALTER TABLE "Expenses" ADD COLUMN "RecurrenceType" INTEGER NULL;
        RAISE NOTICE 'Columna RecurrenceType agregada';
    ELSE
        RAISE NOTICE 'Columna RecurrenceType ya existe';
    END IF;

    -- Agregar columna Tags
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'Expenses' AND column_name = 'Tags'
    ) THEN
        ALTER TABLE "Expenses" ADD COLUMN "Tags" TEXT[] NOT NULL DEFAULT '{}';
        RAISE NOTICE 'Columna Tags agregada';
    ELSE
        RAISE NOTICE 'Columna Tags ya existe';
    END IF;
END $$;

-- Verificar las columnas agregadas
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'Expenses' 
ORDER BY ordinal_position;
