-- Migration 011: Record who performed each diagnosis and consultation type

ALTER TABLE consultation
    ADD COLUMN IF NOT EXISTS performed_by_user_id INTEGER REFERENCES app_user(id),
    ADD COLUMN IF NOT EXISTS consultation_type VARCHAR(50);

-- Backfill existing rows (admin general diagnosis)
UPDATE consultation
SET performed_by_user_id = (
        SELECT id FROM app_user WHERE username = 'admin' LIMIT 1
    ),
    consultation_type = 'ADMIN_GENERAL'
WHERE performed_by_user_id IS NULL;

ALTER TABLE consultation
    ALTER COLUMN performed_by_user_id SET NOT NULL,
    ALTER COLUMN consultation_type SET NOT NULL;

ALTER TABLE consultation
    DROP CONSTRAINT IF EXISTS consultation_type_check;

ALTER TABLE consultation
    ADD CONSTRAINT consultation_type_check
    CHECK (consultation_type IN ('FARMER_SELF', 'ADMIN_FOR_FARMER', 'ADMIN_GENERAL'));
