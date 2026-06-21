-- Migration 009: Roles, users, and farmer profile fields

CREATE TABLE IF NOT EXISTS role (
    id    SERIAL PRIMARY KEY,
    code  VARCHAR(50) NOT NULL UNIQUE,
    label VARCHAR(100) NOT NULL
);

ALTER TABLE farmer
    ADD COLUMN IF NOT EXISTS email VARCHAR(150),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE IF NOT EXISTS app_user (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role_id       INTEGER NOT NULL REFERENCES role(id),
    farmer_id     INTEGER REFERENCES farmer(id) ON DELETE SET NULL,
    full_name     VARCHAR(150),
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
