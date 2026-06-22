-- Full schema: crop disease expert system
-- Run migrations in order, or execute this file for a fresh database.
-- Design: fully normalized, one value per cell, rules via foreign keys only.

\i migrations/001_create_crop_tables.sql
\i migrations/002_create_disease_tables.sql
\i migrations/003_create_symptom_tables.sql
\i migrations/004_create_rule_tables.sql
\i migrations/005_create_consultation_tables.sql
\i migrations/006_create_diagnosis_result_tables.sql
\i migrations/007_create_ai_prediction_tables.sql
\i migrations/008_create_rule_treatment_table.sql
\i migrations/009_create_auth_tables.sql
\i migrations/010_create_consultation_report_table.sql
\i migrations/011_alter_consultation_actor.sql
\i migrations/012_create_consultation_image_table.sql
\i migrations/013_alter_consultation_image_no_storage.sql
\i migrations/014_image_consultation_types.sql
\i migrations/015_consultation_source_match_tier.sql
\i migrations/016_consultation_match_trace.sql
\i migrations/017_create_expert_role.sql
