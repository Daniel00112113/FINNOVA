-- Script de inicialización de la base de datos FINNOVA
-- Se ejecuta automáticamente al crear el contenedor por primera vez

-- Extensión para UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Las tablas principales las crea Entity Framework al arrancar el backend.
-- Este script aplica las migraciones adicionales que EF no maneja.

-- Esperar a que EF cree las tablas base antes de ejecutar esto manualmente
-- o usar el script de migración después del primer arranque del backend.

-- Migración: Tags como array (fix para columna creada por EF como text)
-- Se aplica solo si la columna existe como text
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'Expenses'
          AND column_name = 'Tags'
          AND data_type = 'text'
    ) THEN
        ALTER TABLE "Expenses"
        ALTER COLUMN "Tags" TYPE text[]
        USING CASE
            WHEN "Tags" IS NULL OR "Tags" = '' THEN ARRAY[]::text[]
            ELSE ARRAY["Tags"]
        END;
    END IF;
END $$;

-- Migración: Gamificación
CREATE TABLE IF NOT EXISTS user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "Users"("Id") ON DELETE CASCADE,
    points INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_activity_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_logins INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "Users"("Id") ON DELETE CASCADE,
    type VARCHAR(100) NOT NULL,
    points_earned INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_level ON user_progress(level);
CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON achievements(user_id);

CREATE OR REPLACE FUNCTION update_user_progress_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_user_progress_timestamp ON user_progress;
CREATE TRIGGER trigger_update_user_progress_timestamp
    BEFORE UPDATE ON user_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_user_progress_timestamp();
