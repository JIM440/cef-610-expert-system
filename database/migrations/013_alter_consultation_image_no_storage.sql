-- Migration 013: Store analysis metadata only (no image files in DB or on disk)

ALTER TABLE consultation_image DROP COLUMN IF EXISTS stored_path;

ALTER TABLE consultation_image
    ADD COLUMN IF NOT EXISTS analysis_source VARCHAR(50) NOT NULL DEFAULT 'gemini';
