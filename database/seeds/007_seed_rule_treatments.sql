-- Seed rule_treatment links (one treatment per row per rule)

INSERT INTO rule_treatment (rule_id, treatment_id, priority_level)
SELECT r.id, t.id, x.priority_level
FROM (
    VALUES
        ('EB-Rule-01: Brown spots + yellowing + high humidity', 'Remove infected leaves', 1),
        ('EB-Rule-01: Brown spots + yellowing + high humidity', 'Apply chlorothalonil fungicide', 2),
        ('EB-Rule-01: Brown spots + yellowing + high humidity', 'Improve plant spacing', 3),
        ('LB-Rule-01: Water-soaked lesions + high rainfall', 'Remove infected leaves', 1),
        ('LB-Rule-01: Water-soaked lesions + high rainfall', 'Apply copper-based fungicide', 2),
        ('LB-Rule-01: Water-soaked lesions + high rainfall', 'Isolate infected plants', 3),
        ('SLS-Rule-01: Brown spots + yellowing + moderate humidity', 'Remove infected leaves', 1),
        ('SLS-Rule-01: Brown spots + yellowing + moderate humidity', 'Apply chlorothalonil fungicide', 2),
        ('PM-Rule-01: White coating + dense spacing', 'Apply chlorothalonil fungicide', 1),
        ('PM-Rule-01: White coating + dense spacing', 'Improve plant spacing', 2),
        ('BS-Rule-01: Dark lesions + warm + high rainfall', 'Apply copper-based fungicide', 1),
        ('BS-Rule-01: Dark lesions + warm + high rainfall', 'Reduce overhead irrigation', 2),
        ('TMV-Rule-01: Mosaic pattern + stunted growth', 'Remove infected leaves', 1),
        ('TMV-Rule-01: Mosaic pattern + stunted growth', 'Isolate infected plants', 2),
        ('FW-Rule-01: Wilting + yellowing + warm soil', 'Soil drench with approved fungicide', 1),
        ('FW-Rule-01: Wilting + yellowing + warm soil', 'Use disease-resistant varieties', 2),
        ('BER-Rule-01: Fruit rot + dry soil moisture', 'Apply calcium foliar spray', 1),
        ('BER-Rule-01: Fruit rot + dry soil moisture', 'Reduce overhead irrigation', 2)
) AS x(rule_name, treatment_name, priority_level)
JOIN rule r ON r.rule_name = x.rule_name
JOIN treatment t ON t.name = x.treatment_name
ON CONFLICT (rule_id, treatment_id) DO NOTHING;
