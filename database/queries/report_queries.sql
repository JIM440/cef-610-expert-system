-- Reporting and evaluation queries

-- Disease frequency from consultations
SELECT
    d.name AS disease_name,
    COUNT(c.id) AS consultation_count,
    ROUND(AVG(c.confidence_score), 1) AS avg_confidence
FROM consultation c
JOIN disease d ON d.id = c.diagnosis_disease_id
WHERE c.diagnosis_disease_id IS NOT NULL
GROUP BY d.id, d.name
ORDER BY consultation_count DESC;

-- Most common symptoms across consultations
SELECT
    s.name AS symptom_name,
    COUNT(cs.id) AS occurrence_count
FROM consultation_symptom cs
JOIN symptom s ON s.id = cs.symptom_id
GROUP BY s.id, s.name
ORDER BY occurrence_count DESC;

-- Rule match effectiveness
SELECT
    r.rule_name,
    d.name AS disease_name,
    COUNT(drm.id) AS times_matched,
    ROUND(AVG(drm.matched_score), 1) AS avg_match_score
FROM diagnosis_rule_match drm
JOIN rule r ON r.id = drm.rule_id
JOIN disease d ON d.id = r.disease_id
GROUP BY r.id, r.rule_name, d.name
ORDER BY times_matched DESC;

-- AI vs rule-based agreement
SELECT
    c.id AS consultation_id,
    d_rule.name AS rule_diagnosis,
    d_ai.name AS ai_prediction,
    ap.confidence_score AS ai_confidence,
    CASE WHEN c.diagnosis_disease_id = ap.predicted_disease_id THEN 'Agree' ELSE 'Disagree' END AS agreement
FROM consultation c
JOIN ai_prediction ap ON ap.consultation_id = c.id
LEFT JOIN disease d_rule ON d_rule.id = c.diagnosis_disease_id
JOIN disease d_ai ON d_ai.id = ap.predicted_disease_id
ORDER BY c.consultation_date DESC;
