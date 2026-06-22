\set ON_ERROR_STOP on

-- Add the independent knowledge-base-derived Naive Bayes result to each
-- consultation. This is additive, preserves all data, and keeps 15 tables.
BEGIN;

ALTER TABLE consultation
    ADD COLUMN IF NOT EXISTS ai_predicted_disease_id INTEGER,
    ADD COLUMN IF NOT EXISTS ai_confidence INTEGER,
    ADD COLUMN IF NOT EXISTS ai_model_version VARCHAR(30);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'consultation_ai_predicted_disease_id_fkey'
    ) THEN
        ALTER TABLE consultation
            ADD CONSTRAINT consultation_ai_predicted_disease_id_fkey
            FOREIGN KEY (ai_predicted_disease_id) REFERENCES disease(id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'consultation_ai_confidence_check'
    ) THEN
        ALTER TABLE consultation
            ADD CONSTRAINT consultation_ai_confidence_check
            CHECK (ai_confidence IS NULL OR (ai_confidence >= 0 AND ai_confidence <= 100));
    END IF;
END $$;

COMMIT;
