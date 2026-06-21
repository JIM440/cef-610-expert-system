-- Migration 003: Reason type lookup (for diagnosis explanations)
-- Replaces free-text reason categories with FK references.

CREATE TABLE IF NOT EXISTS reason_type (
    id    SERIAL PRIMARY KEY,
    code  VARCHAR(50) NOT NULL UNIQUE,
    label VARCHAR(150) NOT NULL
);
