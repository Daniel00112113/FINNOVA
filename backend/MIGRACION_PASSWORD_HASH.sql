-- Migración: Asegurar que Users tiene PasswordHash
-- Fecha: 2026-03-08
-- Descripción: Verifica y actualiza la tabla Users para autenticación segura

DO $$ 
BEGIN
    -- Verificar si la columna PasswordHash existe
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'Users' AND column_name = 'PasswordHash'
    ) THEN
        ALTER TABLE "Users" ADD COLUMN "PasswordHash" TEXT NOT NULL DEFAULT '';
        RAISE NOTICE 'Columna PasswordHash agregada';
    ELSE
        RAISE NOTICE 'Columna PasswordHash ya existe';
    END IF;

    -- Marcar usuarios existentes para reset de contraseña
    -- (sus contraseñas actuales no están hasheadas)
    UPDATE "Users" 
    SET "PasswordHash" = '$2a$12$dummy.hash.for.migration.only.change.on.first.login'
    WHERE "PasswordHash" = '' OR "PasswordHash" IS NULL;
    
    RAISE NOTICE 'Usuarios actualizados con hash temporal';
END $$;

-- Verificar estructura
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'Users' 
ORDER BY ordinal_position;
