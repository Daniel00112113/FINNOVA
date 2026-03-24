#!/bin/bash
# Aplica migraciones adicionales después de que el backend haya creado las tablas base
# Uso: ./database/apply-migrations.sh

echo "Esperando que el backend cree las tablas base..."
sleep 15

echo "Aplicando migración de gamificación..."
docker exec financialcopilot-db psql -U postgres -d financialcopilot -f /docker-entrypoint-initdb.d/gamification.sql

echo "Aplicando fix de Tags array..."
docker exec financialcopilot-db psql -U postgres -d financialcopilot -c "
DO \$\$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'Expenses' AND column_name = 'Tags' AND data_type = 'text'
    ) THEN
        ALTER TABLE \"Expenses\" ALTER COLUMN \"Tags\" TYPE text[]
        USING CASE WHEN \"Tags\" IS NULL OR \"Tags\" = '' THEN ARRAY[]::text[] ELSE ARRAY[\"Tags\"] END;
        RAISE NOTICE 'Tags migrado a text[]';
    ELSE
        RAISE NOTICE 'Tags ya es text[], no se necesita migración';
    END IF;
END \$\$;
"

echo "✅ Migraciones aplicadas"
