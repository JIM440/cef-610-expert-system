-- Migration 015: Store consultation source, Gemini extraction, and match tier on consultation

ALTER TABLE consultation
    ADD COLUMN IF NOT EXISTS source VARCHAR(20) NOT NULL DEFAULT 'SYMPTOMS',
    ADD COLUMN IF NOT EXISTS gemini_raw_extraction TEXT,
    ADD COLUMN IF NOT EXISTS match_tier VARCHAR(20) NOT NULL DEFAULT 'HIGH';

UPDATE consultation
SET source = 'IMAGE'
WHERE consultation_type IN ('IMAGE_FARMER_SELF', 'IMAGE_ADMIN_FOR_FARMER', 'IMAGE_ADMIN_GENERAL');

UPDATE consultation c
SET gemini_raw_extraction = COALESCE(ci.analysis_summary, ci.visual_summary)
FROM consultation_image ci
WHERE ci.consultation_id = c.id
  AND c.gemini_raw_extraction IS NULL;

UPDATE consultation
SET match_tier = CASE
    WHEN confidence_score IS NULL THEN 'NONE'
    WHEN confidence_score >= 50 THEN 'HIGH'
    ELSE 'LOW'
END
WHERE match_tier IS NULL OR match_tier = 'HIGH';

ALTER TABLE consultation
    DROP CONSTRAINT IF EXISTS consultation_source_check,
    DROP CONSTRAINT IF EXISTS consultation_match_tier_check;

ALTER TABLE consultation
    ADD CONSTRAINT consultation_source_check CHECK (source IN ('SYMPTOMS', 'IMAGE')),
    ADD CONSTRAINT consultation_match_tier_check CHECK (match_tier IN ('HIGH', 'LOW', 'NONE'));
