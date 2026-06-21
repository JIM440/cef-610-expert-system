-- Migration 004: Expert rules (FK-only; no embedded symptom/condition text)

CREATE TABLE IF NOT EXISTS rule (
    id                SERIAL PRIMARY KEY,
    disease_id        INTEGER NOT NULL REFERENCES disease(id) ON DELETE CASCADE,
    rule_name         VARCHAR(150) NOT NULL,
    confidence_score  INTEGER NOT NULL DEFAULT 70 CHECK (confidence_score BETWEEN 0 AND 100),
    is_active         BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (disease_id, rule_name)
);

CREATE TABLE IF NOT EXISTS rule_symptom (
    id          SERIAL PRIMARY KEY,
    rule_id     INTEGER NOT NULL REFERENCES rule(id) ON DELETE CASCADE,
    symptom_id  INTEGER NOT NULL REFERENCES symptom(id) ON DELETE CASCADE,
    is_required BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (rule_id, symptom_id)
);

CREATE TABLE IF NOT EXISTS rule_environment (
    id                 SERIAL PRIMARY KEY,
    rule_id            INTEGER NOT NULL REFERENCES rule(id) ON DELETE CASCADE,
    condition_value_id INTEGER NOT NULL REFERENCES environmental_condition_value(id) ON DELETE CASCADE,
    is_required        BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (rule_id, condition_value_id)
);
