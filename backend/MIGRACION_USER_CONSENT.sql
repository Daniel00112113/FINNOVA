-- Migración: Agregar tabla de consentimiento para entrenamiento de IA
-- Fecha: 2026-03-06
-- Propósito: Permitir que usuarios opten por compartir sus datos para mejorar la IA

-- Crear tabla de consentimiento
CREATE TABLE IF NOT EXISTS "UserConsent" (
    "UserId" UUID PRIMARY KEY REFERENCES "Users"("Id") ON DELETE CASCADE,
    "AllowDataForTraining" BOOLEAN NOT NULL DEFAULT FALSE,
    "ConsentDate" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ConsentVersion" VARCHAR(10) NOT NULL DEFAULT '1.0',
    "UpdatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS "IX_UserConsent_AllowDataForTraining" 
ON "UserConsent"("AllowDataForTraining");

-- Comentarios
COMMENT ON TABLE "UserConsent" IS 'Almacena el consentimiento de usuarios para usar sus datos en entrenamiento de IA';
COMMENT ON COLUMN "UserConsent"."AllowDataForTraining" IS 'TRUE si el usuario permite usar sus datos para entrenar la IA';
COMMENT ON COLUMN "UserConsent"."ConsentDate" IS 'Fecha en que el usuario dio su consentimiento';
COMMENT ON COLUMN "UserConsent"."ConsentVersion" IS 'Versión del acuerdo de consentimiento';

-- Insertar consentimiento por defecto para usuarios existentes (FALSE por defecto)
INSERT INTO "UserConsent" ("UserId", "AllowDataForTraining", "ConsentDate", "ConsentVersion")
SELECT "Id", FALSE, CURRENT_TIMESTAMP, '1.0'
FROM "Users"
WHERE "Id" NOT IN (SELECT "UserId" FROM "UserConsent")
ON CONFLICT ("UserId") DO NOTHING;

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
SELECT 
    COUNT(*) as total_users,
    SUM(CASE WHEN "AllowDataForTraining" = TRUE THEN 1 ELSE 0 END) as users_with_consent,
    SUM(CASE WHEN "AllowDataForTraining" = FALSE THEN 1 ELSE 0 END) as users_without_consent
FROM "UserConsent";

PRINT 'Migración completada: Tabla UserConsent creada';
