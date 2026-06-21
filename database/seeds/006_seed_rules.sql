-- Seed expert rules: symptoms and conditions linked only by foreign keys

INSERT INTO rule (disease_id, rule_name, confidence_score, is_active)
SELECT d.id, r.rule_name, r.confidence_score, TRUE
FROM (
    VALUES
        ('Early Blight', 'EB-Rule-01: Brown spots + yellowing + high humidity', 85),
        ('Early Blight', 'EB-Rule-02: Brown spots + warm temperature', 75),
        ('Late Blight', 'LB-Rule-01: Water-soaked lesions + high rainfall', 90),
        ('Late Blight', 'LB-Rule-02: Wilting + cool temperature + high humidity', 88),
        ('Septoria Leaf Spot', 'SLS-Rule-01: Brown spots + yellowing + moderate humidity', 80),
        ('Powdery Mildew', 'PM-Rule-01: White coating + dense spacing', 82),
        ('Powdery Mildew', 'PM-Rule-02: White coating + warm temperature', 78),
        ('Bacterial Spot', 'BS-Rule-01: Dark lesions + warm + high rainfall', 83),
        ('Tomato Mosaic Virus', 'TMV-Rule-01: Mosaic pattern + stunted growth', 86),
        ('Fusarium Wilt', 'FW-Rule-01: Wilting + yellowing + warm soil', 84),
        ('Blossom End Rot', 'BER-Rule-01: Fruit rot + dry soil moisture', 80),
        ('Blossom End Rot', 'BER-Rule-02: Fruit rot + waterlogged soil', 76)
) AS r(disease_name, rule_name, confidence_score)
JOIN disease d ON d.name = r.disease_name
ON CONFLICT (disease_id, rule_name) DO NOTHING;

-- Rule required symptoms
INSERT INTO rule_symptom (rule_id, symptom_id, is_required)
SELECT r.id, s.id, TRUE
FROM (
    VALUES
        ('EB-Rule-01: Brown spots + yellowing + high humidity', 'Brown spots on leaves'),
        ('EB-Rule-01: Brown spots + yellowing + high humidity', 'Yellowing leaves'),
        ('EB-Rule-02: Brown spots + warm temperature', 'Brown spots on leaves'),
        ('LB-Rule-01: Water-soaked lesions + high rainfall', 'Dark water-soaked lesions'),
        ('LB-Rule-02: Wilting + cool temperature + high humidity', 'Wilting leaves'),
        ('LB-Rule-02: Wilting + cool temperature + high humidity', 'Dark water-soaked lesions'),
        ('SLS-Rule-01: Brown spots + yellowing + moderate humidity', 'Brown spots on leaves'),
        ('SLS-Rule-01: Brown spots + yellowing + moderate humidity', 'Yellowing leaves'),
        ('PM-Rule-01: White coating + dense spacing', 'White powdery coating'),
        ('PM-Rule-02: White coating + warm temperature', 'White powdery coating'),
        ('BS-Rule-01: Dark lesions + warm + high rainfall', 'Dark water-soaked lesions'),
        ('TMV-Rule-01: Mosaic pattern + stunted growth', 'Mosaic leaf pattern'),
        ('TMV-Rule-01: Mosaic pattern + stunted growth', 'Stunted growth'),
        ('FW-Rule-01: Wilting + yellowing + warm soil', 'Wilting leaves'),
        ('FW-Rule-01: Wilting + yellowing + warm soil', 'Yellowing leaves'),
        ('BER-Rule-01: Fruit rot + dry soil moisture', 'Fruit rot at blossom end'),
        ('BER-Rule-02: Fruit rot + waterlogged soil', 'Fruit rot at blossom end')
) AS x(rule_name, symptom_name)
JOIN rule r ON r.rule_name = x.rule_name
JOIN symptom s ON s.name = x.symptom_name
ON CONFLICT (rule_id, symptom_id) DO NOTHING;

-- Rule required environmental conditions
INSERT INTO rule_environment (rule_id, condition_value_id, is_required)
SELECT r.id, ecv.id, TRUE
FROM (
    VALUES
        ('EB-Rule-01: Brown spots + yellowing + high humidity', 'Humidity', 'High'),
        ('EB-Rule-02: Brown spots + warm temperature', 'Temperature', 'Warm'),
        ('LB-Rule-01: Water-soaked lesions + high rainfall', 'Rainfall', 'High'),
        ('LB-Rule-02: Wilting + cool temperature + high humidity', 'Temperature', 'Cool'),
        ('LB-Rule-02: Wilting + cool temperature + high humidity', 'Humidity', 'High'),
        ('SLS-Rule-01: Brown spots + yellowing + moderate humidity', 'Humidity', 'Moderate'),
        ('PM-Rule-01: White coating + dense spacing', 'Plant spacing', 'Dense'),
        ('PM-Rule-02: White coating + warm temperature', 'Temperature', 'Warm'),
        ('BS-Rule-01: Dark lesions + warm + high rainfall', 'Temperature', 'Warm'),
        ('BS-Rule-01: Dark lesions + warm + high rainfall', 'Rainfall', 'High'),
        ('FW-Rule-01: Wilting + yellowing + warm soil', 'Temperature', 'Warm'),
        ('BER-Rule-01: Fruit rot + dry soil moisture', 'Soil moisture', 'Dry'),
        ('BER-Rule-02: Fruit rot + waterlogged soil', 'Soil moisture', 'Waterlogged')
) AS x(rule_name, condition_name, value_name)
JOIN rule r ON r.rule_name = x.rule_name
JOIN environmental_condition ec ON ec.name = x.condition_name
JOIN environmental_condition_value ecv ON ecv.condition_id = ec.id AND ecv.value_name = x.value_name
ON CONFLICT (rule_id, condition_value_id) DO NOTHING;
