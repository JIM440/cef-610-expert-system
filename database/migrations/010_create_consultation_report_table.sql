-- Migration 010: Editable report metadata before PDF export

CREATE TABLE IF NOT EXISTS consultation_report (
    id               SERIAL PRIMARY KEY,
    consultation_id  INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    report_title     VARCHAR(200) NOT NULL,
    summary          TEXT,
    notes            TEXT,
    recommendations  TEXT,
    generated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
