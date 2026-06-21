-- Seed environmental conditions and discrete values (one value per row)

INSERT INTO environmental_condition (name, unit) VALUES
    ('Humidity', 'level'),
    ('Temperature', 'level'),
    ('Rainfall', 'level'),
    ('Soil moisture', 'level'),
    ('Plant spacing', 'density')
ON CONFLICT (name) DO NOTHING;

INSERT INTO environmental_condition_value (condition_id, value_name)
SELECT ec.id, v.value_name
FROM environmental_condition ec
CROSS JOIN (
    VALUES
        ('Humidity', 'Low'),
        ('Humidity', 'Moderate'),
        ('Humidity', 'High'),
        ('Temperature', 'Cool'),
        ('Temperature', 'Warm'),
        ('Temperature', 'Hot'),
        ('Rainfall', 'Low'),
        ('Rainfall', 'Moderate'),
        ('Rainfall', 'High'),
        ('Soil moisture', 'Dry'),
        ('Soil moisture', 'Adequate'),
        ('Soil moisture', 'Waterlogged'),
        ('Plant spacing', 'Dense'),
        ('Plant spacing', 'Normal'),
        ('Plant spacing', 'Wide')
) AS v(condition_name, value_name)
WHERE ec.name = v.condition_name
ON CONFLICT (condition_id, value_name) DO NOTHING;

-- Reason types for diagnosis explanations (FK lookup, not free-text categories)
INSERT INTO reason_type (code, label) VALUES
    ('symptom_match', 'Matching symptom observed'),
    ('environment_match', 'Supporting environmental condition'),
    ('rule_match', 'Expert rule matched'),
    ('ai_prediction', 'AI model prediction'),
    ('treatment_recommendation', 'Recommended treatment')
ON CONFLICT (code) DO NOTHING;
