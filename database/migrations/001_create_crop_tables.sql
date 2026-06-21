-- Migration 001: Core crop entity
-- One row per crop; no arrays or JSON.

CREATE TABLE IF NOT EXISTS crop (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);
