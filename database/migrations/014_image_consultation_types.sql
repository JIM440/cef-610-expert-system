-- Migration 014: Separate image-recognition consultations from symptom-based diagnosis

ALTER TABLE consultation
    DROP CONSTRAINT IF EXISTS consultation_type_check;

ALTER TABLE consultation
    ADD CONSTRAINT consultation_type_check
    CHECK (consultation_type IN (
        'FARMER_SELF', 'ADMIN_FOR_FARMER', 'ADMIN_GENERAL',
        'IMAGE_FARMER_SELF', 'IMAGE_ADMIN_FOR_FARMER', 'IMAGE_ADMIN_GENERAL'
    ));

ALTER TABLE consultation_image
    ADD COLUMN IF NOT EXISTS visual_summary TEXT,
    ADD COLUMN IF NOT EXISTS gemini_model VARCHAR(100);
