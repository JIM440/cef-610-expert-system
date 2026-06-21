-- Migration 002: Diseases and disease knowledge links

CREATE TABLE IF NOT EXISTS disease (
    id                    SERIAL PRIMARY KEY,
    crop_id               INTEGER NOT NULL REFERENCES crop(id) ON DELETE CASCADE,
    name                  VARCHAR(150) NOT NULL,
    description           TEXT,
    explanation_template  TEXT,
    UNIQUE (crop_id, name)
);

CREATE TABLE IF NOT EXISTS symptom (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS environmental_condition (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL UNIQUE,
    unit        VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS environmental_condition_value (
    id           SERIAL PRIMARY KEY,
    condition_id INTEGER NOT NULL REFERENCES environmental_condition(id) ON DELETE CASCADE,
    value_name   VARCHAR(100) NOT NULL,
    UNIQUE (condition_id, value_name)
);

CREATE TABLE IF NOT EXISTS disease_symptom (
    id         SERIAL PRIMARY KEY,
    disease_id INTEGER NOT NULL REFERENCES disease(id) ON DELETE CASCADE,
    symptom_id INTEGER NOT NULL REFERENCES symptom(id) ON DELETE CASCADE,
    weight     INTEGER NOT NULL DEFAULT 1 CHECK (weight BETWEEN 1 AND 10),
    UNIQUE (disease_id, symptom_id)
);

CREATE TABLE IF NOT EXISTS disease_environment (
    id                 SERIAL PRIMARY KEY,
    disease_id         INTEGER NOT NULL REFERENCES disease(id) ON DELETE CASCADE,
    condition_value_id INTEGER NOT NULL REFERENCES environmental_condition_value(id) ON DELETE CASCADE,
    weight             INTEGER NOT NULL DEFAULT 1 CHECK (weight BETWEEN 1 AND 10),
    UNIQUE (disease_id, condition_value_id)
);

CREATE TABLE IF NOT EXISTS treatment (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS disease_treatment (
    id             SERIAL PRIMARY KEY,
    disease_id     INTEGER NOT NULL REFERENCES disease(id) ON DELETE CASCADE,
    treatment_id   INTEGER NOT NULL REFERENCES treatment(id) ON DELETE CASCADE,
    priority_level INTEGER NOT NULL DEFAULT 1 CHECK (priority_level BETWEEN 1 AND 5),
    UNIQUE (disease_id, treatment_id)
);
