-- Migración simplificada: UserConsent
-- No requiere tabla Users existente

-- Crear tabla de consentimiento (sin foreign key por ahora)
CREATE TABLE IF NOT EXISTS "UserConsent" (
    "UserId" UUID PRIMARY KEY,
    "AllowDataForTraining" BOOLEAN NOT NULL DEFAULT FALSE,
    "ConsentDate" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ConsentVersion" VARCHAR(10) NOT NULL DEFAULT '1.0',
    "UpdatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS "IX_UserConsent_AllowDataForTraining" 
ON "UserConsent"("AllowDataForTraining");

-- Función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION update_user_consent_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW."UpdatedAt" = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar timestamp
DROP TRIGGER IF EXISTS trigger_update_user_consent_timestamp ON "UserConsent";
CREATE TRIGGER trigger_update_user_consent_timestamp
    BEFORE UPDATE ON "UserConsent"
    FOR EACH ROW
    EXECUTE FUNCTION update_user_consent_timestamp();

-- Verificar
SELECT COUNT(*) as total_records FROM "UserConsent";
