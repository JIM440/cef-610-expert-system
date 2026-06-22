\set ON_ERROR_STOP on

-- Crop Disease Expert System: destructive consolidation from 29 to 15 tables.
-- Run:
--   psql -U postgres -d crop_expert_system -f database/consolidate_29_to_15.sql
--
-- IMPORTANT: this migration intentionally drops disease_environment and
-- disease_treatment, including relationships that do not exist in rule tables.

BEGIN;

DO $$
DECLARE
    missing_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO missing_count
    FROM (
        VALUES
            ('app_user'), ('consultation'), ('farmer'), ('role'),
            ('environmental_condition'), ('environmental_condition_value'),
            ('diagnosis_result'), ('rule')
    ) expected(table_name)
    WHERE to_regclass('public.' || expected.table_name) IS NULL;

    IF missing_count > 0 THEN
        RAISE EXCEPTION 'Consolidation preflight failed: expected legacy tables are missing';
    END IF;
END $$;

\echo 'Pre-migration row counts'
SELECT relname AS table_name, n_live_tup::bigint AS estimated_rows
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY relname;

CREATE TABLE environmental_factor (
    id         SERIAL PRIMARY KEY,
    category   VARCHAR(30) NOT NULL,
    value_name VARCHAR(100) NOT NULL,
    unit       VARCHAR(20),
    UNIQUE (category, value_name)
);

INSERT INTO environmental_factor (id, category, value_name, unit)
SELECT ecv.id, ec.name, ecv.value_name, ec.unit
FROM environmental_condition_value ecv
JOIN environmental_condition ec ON ec.id = ecv.condition_id
ORDER BY ecv.id;

SELECT setval(
    pg_get_serial_sequence('environmental_factor', 'id'),
    COALESCE((SELECT MAX(id) FROM environmental_factor), 1),
    TRUE
);

ALTER TABLE app_user
    ALTER COLUMN username DROP NOT NULL,
    ALTER COLUMN password_hash DROP NOT NULL,
    ADD COLUMN role VARCHAR(10),
    ADD COLUMN phone_number VARCHAR(20),
    ADD COLUMN location VARCHAR(100),
    ADD COLUMN email VARCHAR(100),
    ADD COLUMN updated_at TIMESTAMP,
    ADD COLUMN legacy_farmer_id INTEGER;

UPDATE app_user u
SET role = UPPER(r.code),
    legacy_farmer_id = u.farmer_id,
    updated_at = CURRENT_TIMESTAMP
FROM role r
WHERE r.id = u.role_id;

UPDATE app_user u
SET full_name = COALESCE(f.full_name, u.full_name),
    phone_number = f.phone_number,
    location = f.location,
    email = f.email,
    updated_at = COALESCE(f.updated_at, f.created_at, CURRENT_TIMESTAMP)
FROM farmer f
WHERE f.id = u.farmer_id;

INSERT INTO app_user (
    username, password_hash, full_name, is_active, created_at,
    role, phone_number, location, email, updated_at, legacy_farmer_id,
    role_id, farmer_id
)
SELECT
    NULL, NULL, f.full_name, TRUE, f.created_at,
    'FARMER', f.phone_number, f.location, f.email,
    COALESCE(f.updated_at, f.created_at), f.id,
    (SELECT id FROM role WHERE code = 'farmer'), f.id
FROM farmer f
WHERE NOT EXISTS (
    SELECT 1 FROM app_user u WHERE u.farmer_id = f.id
);

ALTER TABLE consultation
    ADD COLUMN matched_rule_id INTEGER,
    ADD COLUMN explanation TEXT;

UPDATE consultation c
SET matched_rule_id = COALESCE(
        (
            SELECT drm.rule_id
            FROM diagnosis_result dr
            JOIN diagnosis_rule_match drm ON drm.diagnosis_result_id = dr.id
            WHERE dr.consultation_id = c.id
            ORDER BY drm.matched_score DESC NULLS LAST, drm.id
            LIMIT 1
        ),
        (
            SELECT dre.related_rule_id
            FROM diagnosis_result dr
            JOIN diagnosis_reason dre ON dre.diagnosis_result_id = dr.id
            WHERE dr.consultation_id = c.id
              AND dre.related_rule_id IS NOT NULL
            ORDER BY dre.display_order, dre.id
            LIMIT 1
        )
    ),
    explanation = (
        SELECT dr.explanation
        FROM diagnosis_result dr
        WHERE dr.consultation_id = c.id
        ORDER BY dr.id
        LIMIT 1
    );

UPDATE consultation_symptom cs
SET matched = TRUE
WHERE EXISTS (
    SELECT 1
    FROM diagnosis_result dr
    JOIN diagnosis_reason dre ON dre.diagnosis_result_id = dr.id
    JOIN diagnosis_reason_symptom drs ON drs.diagnosis_reason_id = dre.id
    WHERE dr.consultation_id = cs.consultation_id
      AND drs.symptom_id = cs.symptom_id
);

UPDATE consultation_environment ce
SET matched = TRUE
WHERE EXISTS (
    SELECT 1
    FROM diagnosis_result dr
    JOIN diagnosis_reason dre ON dre.diagnosis_result_id = dr.id
    JOIN diagnosis_reason_environment dre_env
      ON dre_env.diagnosis_reason_id = dre.id
    WHERE dr.consultation_id = ce.consultation_id
      AND dre_env.condition_value_id = ce.condition_value_id
);

ALTER TABLE rule_environment
    DROP CONSTRAINT rule_environment_condition_value_id_fkey,
    DROP CONSTRAINT rule_environment_rule_id_condition_value_id_key;

ALTER TABLE consultation_environment
    DROP CONSTRAINT consultation_environment_condition_value_id_fkey,
    DROP CONSTRAINT consultation_environment_consultation_id_condition_value_id_key;

ALTER TABLE rule_environment
    RENAME COLUMN condition_value_id TO environmental_factor_id;

ALTER TABLE consultation_environment
    RENAME COLUMN condition_value_id TO environmental_factor_id;

ALTER TABLE rule_environment
    ADD CONSTRAINT rule_environment_environmental_factor_id_fkey
        FOREIGN KEY (environmental_factor_id)
        REFERENCES environmental_factor(id) ON DELETE CASCADE,
    ADD CONSTRAINT rule_environment_rule_factor_key
        UNIQUE (rule_id, environmental_factor_id);

ALTER TABLE consultation_environment
    ADD CONSTRAINT consultation_environment_environmental_factor_id_fkey
        FOREIGN KEY (environmental_factor_id)
        REFERENCES environmental_factor(id),
    ADD CONSTRAINT consultation_environment_consultation_factor_key
        UNIQUE (consultation_id, environmental_factor_id);

ALTER TABLE consultation
    DROP CONSTRAINT consultation_farmer_id_fkey;

UPDATE consultation c
SET farmer_id = u.id
FROM app_user u
WHERE u.legacy_farmer_id = c.farmer_id;

ALTER TABLE consultation
    ADD CONSTRAINT consultation_farmer_id_fkey
        FOREIGN KEY (farmer_id) REFERENCES app_user(id) ON DELETE SET NULL,
    ADD CONSTRAINT consultation_matched_rule_id_fkey
        FOREIGN KEY (matched_rule_id) REFERENCES rule(id) ON DELETE SET NULL;

ALTER TABLE consultation
    RENAME COLUMN diagnosis_disease_id TO final_disease_id;

ALTER TABLE consultation
    RENAME COLUMN confidence_score TO final_confidence;

ALTER TABLE app_user
    DROP CONSTRAINT app_user_role_id_fkey,
    DROP CONSTRAINT app_user_farmer_id_fkey,
    DROP COLUMN role_id,
    DROP COLUMN farmer_id,
    DROP COLUMN legacy_farmer_id,
    ALTER COLUMN role SET DEFAULT 'FARMER',
    ALTER COLUMN role SET NOT NULL,
    ADD CONSTRAINT app_user_role_check
        CHECK (role IN ('ADMIN', 'EXPERT', 'FARMER')),
    ADD CONSTRAINT chk_admin_has_login
        CHECK (role != 'ADMIN' OR (username IS NOT NULL AND password_hash IS NOT NULL));

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM consultation
        WHERE performed_by_user_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Consolidation failed: consultation performer became null';
    END IF;

    IF EXISTS (
        SELECT 1 FROM rule_environment re
        LEFT JOIN environmental_factor ef ON ef.id = re.environmental_factor_id
        WHERE ef.id IS NULL
    ) OR EXISTS (
        SELECT 1 FROM consultation_environment ce
        LEFT JOIN environmental_factor ef ON ef.id = ce.environmental_factor_id
        WHERE ef.id IS NULL
    ) THEN
        RAISE EXCEPTION 'Consolidation failed: environmental factor mapping has orphans';
    END IF;

    IF EXISTS (
        SELECT 1 FROM app_user WHERE role IS NULL
    ) THEN
        RAISE EXCEPTION 'Consolidation failed: app_user role was not populated';
    END IF;
END $$;

DROP TABLE diagnosis_rule_match;
DROP TABLE diagnosis_reason_environment;
DROP TABLE diagnosis_reason_symptom;
DROP TABLE diagnosis_reason;
DROP TABLE reason_type;
DROP TABLE diagnosis_result;
DROP TABLE consultation_image;
DROP TABLE consultation_report;
DROP TABLE ai_prediction;
DROP TABLE disease_environment;
DROP TABLE disease_treatment;
DROP TABLE environmental_condition_value;
DROP TABLE environmental_condition;
DROP TABLE farmer;
DROP TABLE role;

DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE';

    IF table_count != 15 THEN
        RAISE EXCEPTION 'Expected 15 tables after consolidation, found %', table_count;
    END IF;
END $$;

COMMIT;

\echo 'Post-migration row counts'
SELECT relname AS table_name, n_live_tup::bigint AS estimated_rows
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY relname;

/*
ROLLBACK / DOWN MIGRATION REFERENCE
===================================
The dropped explanation, role, farmer, disease fact, image, report, and AI
tables cannot be reconstructed losslessly from the 15-table result because
the approved migration intentionally discards unmatched disease facts and
report history. The supported rollback is:

1. Stop application writes.
2. Drop the migrated database.
3. Restore the pre-migration pg_dump backup:

   dropdb -U postgres crop_expert_system
   createdb -U postgres crop_expert_system
   pg_restore -U postgres -d crop_expert_system crop_expert_system_pre_consolidation.dump

This file is transactional, so any failure before COMMIT automatically
restores the original 29-table schema.
*/
