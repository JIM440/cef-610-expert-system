-- Migration 005: Farmers and consultations (one value per cell via junction tables)

CREATE TABLE IF NOT EXISTS farmer (
    id           SERIAL PRIMARY KEY,
    full_name    VARCHAR(150),
    phone_number VARCHAR(30),
    location     VARCHAR(150),
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consultation (
    id                   SERIAL PRIMARY KEY,
    farmer_id            INTEGER REFERENCES farmer(id) ON DELETE SET NULL,
    crop_id              INTEGER NOT NULL REFERENCES crop(id),
    diagnosis_disease_id INTEGER REFERENCES disease(id),
    confidence_score     INTEGER CHECK (confidence_score BETWEEN 0 AND 100),
    consultation_date    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consultation_symptom (
    id               SERIAL PRIMARY KEY,
    consultation_id  INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    symptom_id       INTEGER NOT NULL REFERENCES symptom(id),
    UNIQUE (consultation_id, symptom_id)
);

CREATE TABLE IF NOT EXISTS consultation_environment (
    id                 SERIAL PRIMARY KEY,
    consultation_id    INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    condition_value_id INTEGER NOT NULL REFERENCES environmental_condition_value(id),
    UNIQUE (consultation_id, condition_value_id)
);

CREATE TABLE IF NOT EXISTS consultation_treatment (
    id              SERIAL PRIMARY KEY,
    consultation_id INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    treatment_id    INTEGER NOT NULL REFERENCES treatment(id),
    UNIQUE (consultation_id, treatment_id)
);
