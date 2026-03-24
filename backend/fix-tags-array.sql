-- Fix Tags column from text to text[]
ALTER TABLE "Expenses" 
ALTER COLUMN "Tags" TYPE text[] 
USING CASE 
    WHEN "Tags" IS NULL OR "Tags" = '' THEN ARRAY[]::text[] 
    ELSE ARRAY["Tags"] 
END;
