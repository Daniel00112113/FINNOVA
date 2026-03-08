-- Actualizar registros existentes con Tags NULL
UPDATE "Expenses" SET "Tags" = '' WHERE "Tags" IS NULL;
UPDATE "Expenses" SET "Location" = '' WHERE "Location" IS NULL;
UPDATE "Expenses" SET "RecurrenceType" = NULL WHERE "RecurrenceType" = '';
