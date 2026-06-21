-- Migration 007: AI model predictions linked to consultations

CREATE TABLE IF NOT EXISTS ai_prediction (
    id                   SERIAL PRIMARY KEY,
    consultation_id      INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    predicted_disease_id INTEGER NOT NULL REFERENCES disease(id),
    confidence_score     INTEGER CHECK (confidence_score BETWEEN 0 AND 100),
    model_name           VARCHAR(100) NOT NULL,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
