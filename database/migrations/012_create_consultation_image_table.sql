-- Migration 012: Image recognition uploads linked to consultations

CREATE TABLE IF NOT EXISTS consultation_image (
    id                SERIAL PRIMARY KEY,
    consultation_id   INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    original_filename VARCHAR(255) NOT NULL,
    analysis_summary  TEXT,
    visual_summary    TEXT,
    analysis_source   VARCHAR(50) NOT NULL DEFAULT 'gemini',
    gemini_model      VARCHAR(100),
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
