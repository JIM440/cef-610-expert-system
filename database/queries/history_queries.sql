-- Consultation history queries

-- List recent consultations with farmer and diagnosis summary
SELECT
    c.id AS consultation_id,
    c.consultation_date,
    c.consultation_type,
    u.username AS performed_by,
    u.full_name AS performed_by_name,
    f.full_name AS farmer_name,
    f.location,
    cr.name AS crop_name,
    d.name AS diagnosed_disease,
    c.confidence_score,
    dr.explanation
FROM consultation c
JOIN app_user u ON u.id = c.performed_by_user_id
LEFT JOIN farmer f ON f.id = c.farmer_id
JOIN crop cr ON cr.id = c.crop_id
LEFT JOIN disease d ON d.id = c.diagnosis_disease_id
LEFT JOIN diagnosis_result dr ON dr.consultation_id = c.id
ORDER BY c.consultation_date DESC;

-- Symptoms recorded per consultation
-- Parameters: :consultation_id
SELECT s.id, s.name, s.description
FROM consultation_symptom cs
JOIN symptom s ON s.id = cs.symptom_id
WHERE cs.consultation_id = :consultation_id
ORDER BY s.name;

-- Environmental conditions recorded per consultation
-- Parameters: :consultation_id
SELECT
    ec.id AS condition_id,
    ec.name AS condition_name,
    ecv.id AS value_id,
    ecv.value_name
FROM consultation_environment ce
JOIN environmental_condition_value ecv ON ecv.id = ce.condition_value_id
JOIN environmental_condition ec ON ec.id = ecv.condition_id
WHERE ce.consultation_id = :consultation_id
ORDER BY ec.name;
