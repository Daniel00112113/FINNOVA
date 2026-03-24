-- Migración: Agregar Gamificación
-- Fecha: 2026-03-11

-- Tabla de Progreso de Usuario
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

-- Tabla de Logros
CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "Users"("Id") ON DELETE CASCADE,
    type VARCHAR(100) NOT NULL,
    points_earned INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_level ON user_progress(level);
CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON achievements(user_id);

-- Trigger para updated_at
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
