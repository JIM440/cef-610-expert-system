-- Migration 006: Diagnosis results, explanations, and traceable reasons (FK-based)

CREATE TABLE IF NOT EXISTS diagnosis_result (
    id               SERIAL PRIMARY KEY,
    consultation_id  INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    disease_id       INTEGER NOT NULL REFERENCES disease(id),
    result_title     VARCHAR(150) NOT NULL,
    explanation      TEXT NOT NULL,
    confidence_score INTEGER CHECK (confidence_score BETWEEN 0 AND 100),
    created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diagnosis_reason (
    id                  SERIAL PRIMARY KEY,
    diagnosis_result_id INTEGER NOT NULL REFERENCES diagnosis_result(id) ON DELETE CASCADE,
    reason_type_id      INTEGER NOT NULL REFERENCES reason_type(id),
    related_rule_id     INTEGER REFERENCES rule(id) ON DELETE SET NULL,
    display_order       INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS diagnosis_reason_symptom (
    id                  SERIAL PRIMARY KEY,
    diagnosis_reason_id INTEGER NOT NULL REFERENCES diagnosis_reason(id) ON DELETE CASCADE,
    symptom_id          INTEGER NOT NULL REFERENCES symptom(id),
    UNIQUE (diagnosis_reason_id, symptom_id)
);

CREATE TABLE IF NOT EXISTS diagnosis_reason_environment (
    id                  SERIAL PRIMARY KEY,
    diagnosis_reason_id INTEGER NOT NULL REFERENCES diagnosis_reason(id) ON DELETE CASCADE,
    condition_value_id  INTEGER NOT NULL REFERENCES environmental_condition_value(id),
    UNIQUE (diagnosis_reason_id, condition_value_id)
);

CREATE TABLE IF NOT EXISTS diagnosis_rule_match (
    id                  SERIAL PRIMARY KEY,
    diagnosis_result_id INTEGER NOT NULL REFERENCES diagnosis_result(id) ON DELETE CASCADE,
    rule_id             INTEGER NOT NULL REFERENCES rule(id),
    matched_score       INTEGER CHECK (matched_score BETWEEN 0 AND 100),
    UNIQUE (diagnosis_result_id, rule_id)
);
