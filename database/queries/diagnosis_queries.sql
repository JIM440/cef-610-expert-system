-- Reusable diagnosis queries (FK joins; no array/JSON storage)

-- Fetch all active rules for a crop with linked symptoms and conditions
-- Parameters: :crop_id
SELECT
    r.id AS rule_id,
    r.rule_name,
    r.confidence_score,
    d.id AS disease_id,
    d.name AS disease_name,
    d.explanation_template,
    rs.symptom_id,
    s.name AS symptom_name,
    rs.is_required AS symptom_required,
    re.condition_value_id,
    ec.name AS condition_name,
    ecv.value_name AS condition_value,
    re.is_required AS condition_required
FROM rule r
JOIN disease d ON d.id = r.disease_id
LEFT JOIN rule_symptom rs ON rs.rule_id = r.id
LEFT JOIN symptom s ON s.id = rs.symptom_id
LEFT JOIN rule_environment re ON re.rule_id = r.id
LEFT JOIN environmental_condition_value ecv ON ecv.id = re.condition_value_id
LEFT JOIN environmental_condition ec ON ec.id = ecv.condition_id
WHERE d.crop_id = :crop_id
  AND r.is_active = TRUE
ORDER BY r.id, rs.symptom_id, re.condition_value_id;

-- Fetch full diagnosis result with reasons for a consultation
-- Parameters: :consultation_id
SELECT
    dr.id AS diagnosis_result_id,
    dr.result_title,
    dr.explanation,
    dr.confidence_score,
    dis.name AS disease_name,
    dis.description AS disease_description,
    dre.id AS reason_id,
    rt.code AS reason_type_code,
    rt.label AS reason_type_label,
    drm.rule_id,
    ru.rule_name,
    drm.matched_score,
    drs.symptom_id,
    sym.name AS reason_symptom_name,
    dre_env.condition_value_id,
    ec.name AS reason_condition_name,
    ecv.value_name AS reason_condition_value
FROM diagnosis_result dr
JOIN disease dis ON dis.id = dr.disease_id
LEFT JOIN diagnosis_reason dre ON dre.diagnosis_result_id = dr.id
LEFT JOIN reason_type rt ON rt.id = dre.reason_type_id
LEFT JOIN diagnosis_rule_match drm ON drm.diagnosis_result_id = dr.id
LEFT JOIN rule ru ON ru.id = drm.rule_id
LEFT JOIN diagnosis_reason_symptom drs ON drs.diagnosis_reason_id = dre.id
LEFT JOIN symptom sym ON sym.id = drs.symptom_id
LEFT JOIN diagnosis_reason_environment dre_env ON dre_env.diagnosis_reason_id = dre.id
LEFT JOIN environmental_condition_value ecv ON ecv.id = dre_env.condition_value_id
LEFT JOIN environmental_condition ec ON ec.id = ecv.condition_id
WHERE dr.consultation_id = :consultation_id
ORDER BY dre.display_order, drs.symptom_id;

-- Treatments recommended for a consultation
-- Parameters: :consultation_id
SELECT
    t.id,
    t.name,
    t.description
FROM consultation_treatment ct
JOIN treatment t ON t.id = ct.treatment_id
WHERE ct.consultation_id = :consultation_id
ORDER BY t.name;
