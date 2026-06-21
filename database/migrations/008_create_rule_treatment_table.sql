-- Migration 008: Rule-level treatment recommendations (FK-only)

CREATE TABLE IF NOT EXISTS rule_treatment (
    id             SERIAL PRIMARY KEY,
    rule_id        INTEGER NOT NULL REFERENCES rule(id) ON DELETE CASCADE,
    treatment_id   INTEGER NOT NULL REFERENCES treatment(id) ON DELETE CASCADE,
    priority_level INTEGER NOT NULL DEFAULT 1 CHECK (priority_level BETWEEN 1 AND 5),
    UNIQUE (rule_id, treatment_id)
);
