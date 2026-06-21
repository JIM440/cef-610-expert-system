-- Migration 016: Mark which submitted facts contributed to the selected rule.

ALTER TABLE consultation_symptom
    ADD COLUMN IF NOT EXISTS matched BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE consultation_environment
    ADD COLUMN IF NOT EXISTS matched BOOLEAN NOT NULL DEFAULT FALSE;

UPDATE consultation_symptom cs
SET matched = TRUE
FROM diagnosis_result dr
JOIN diagnosis_rule_match drm ON drm.diagnosis_result_id = dr.id
JOIN rule_symptom rs ON rs.rule_id = drm.rule_id
WHERE dr.consultation_id = cs.consultation_id
  AND rs.symptom_id = cs.symptom_id;

UPDATE consultation_environment ce
SET matched = TRUE
FROM diagnosis_result dr
JOIN diagnosis_rule_match drm ON drm.diagnosis_result_id = dr.id
JOIN rule_environment re ON re.rule_id = drm.rule_id
WHERE dr.consultation_id = ce.consultation_id
  AND re.condition_value_id = ce.condition_value_id;
