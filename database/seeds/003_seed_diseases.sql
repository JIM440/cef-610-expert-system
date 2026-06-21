-- Seed tomato diseases and link symptoms, environment, treatments via FKs

INSERT INTO disease (crop_id, name, description, explanation_template)
SELECT c.id, d.name, d.description, d.explanation_template
FROM crop c
CROSS JOIN (
    VALUES
        ('Early Blight', 'Fungal disease caused by Alternaria solani affecting leaves and fruit.',
         'Early Blight is likely because brown leaf spots, yellowing, and warm humid conditions match known Alternaria patterns.'),
        ('Late Blight', 'Destructive oomycete disease (Phytophthora infestans) spreading rapidly in cool wet weather.',
         'Late Blight is likely because water-soaked lesions and high rainfall with cool temperatures favor Phytophthora infestans.'),
        ('Septoria Leaf Spot', 'Fungal leaf spot disease with small circular lesions and dark borders.',
         'Septoria Leaf Spot is likely because brown spots with yellowing on lower leaves appear under moderate humidity.'),
        ('Powdery Mildew', 'Fungal disease producing white powdery patches on leaves.',
         'Powdery Mildew is likely because white powdery coating on leaves occurs in warm dry conditions with dense planting.'),
        ('Bacterial Spot', 'Bacterial disease causing dark lesions on leaves and fruit.',
         'Bacterial Spot is likely because dark greasy lesions spread during warm wet periods with overhead watering.'),
        ('Tomato Mosaic Virus', 'Viral disease causing mosaic patterns and stunted growth.',
         'Tomato Mosaic Virus is likely because mosaic discoloration and stunting indicate viral infection.'),
        ('Fusarium Wilt', 'Soil-borne fungal wilt affecting vascular tissue.',
         'Fusarium Wilt is likely because wilting with yellowing progresses despite adequate moisture in warm soil.'),
        ('Blossom End Rot', 'Physiological disorder linked to calcium transport and uneven watering.',
         'Blossom End Rot is likely because fruit bottom rot appears with fluctuating soil moisture and calcium stress.')
) AS d(name, description, explanation_template)
WHERE c.name = 'Tomato'
ON CONFLICT (crop_id, name) DO NOTHING;

-- Disease-symptom links
INSERT INTO disease_symptom (disease_id, symptom_id, weight)
SELECT d.id, s.id, x.weight
FROM (
    VALUES
        ('Early Blight', 'Brown spots on leaves', 3),
        ('Early Blight', 'Yellowing leaves', 2),
        ('Early Blight', 'Leaf drop', 2),
        ('Late Blight', 'Dark water-soaked lesions', 4),
        ('Late Blight', 'Wilting leaves', 3),
        ('Late Blight', 'Stem cankers', 2),
        ('Septoria Leaf Spot', 'Brown spots on leaves', 3),
        ('Septoria Leaf Spot', 'Yellowing leaves', 2),
        ('Septoria Leaf Spot', 'Leaf drop', 1),
        ('Powdery Mildew', 'White powdery coating', 4),
        ('Powdery Mildew', 'Leaf curling', 2),
        ('Powdery Mildew', 'Stunted growth', 1),
        ('Bacterial Spot', 'Dark water-soaked lesions', 3),
        ('Bacterial Spot', 'Yellowing leaves', 2),
        ('Bacterial Spot', 'Leaf drop', 1),
        ('Tomato Mosaic Virus', 'Mosaic leaf pattern', 4),
        ('Tomato Mosaic Virus', 'Stunted growth', 3),
        ('Tomato Mosaic Virus', 'Leaf curling', 2),
        ('Fusarium Wilt', 'Wilting leaves', 4),
        ('Fusarium Wilt', 'Yellowing leaves', 3),
        ('Fusarium Wilt', 'Purple leaf veins', 2),
        ('Blossom End Rot', 'Fruit rot at blossom end', 4),
        ('Blossom End Rot', 'Stunted growth', 1)
) AS x(disease_name, symptom_name, weight)
JOIN disease d ON d.name = x.disease_name
JOIN symptom s ON s.name = x.symptom_name
ON CONFLICT (disease_id, symptom_id) DO NOTHING;

-- Disease-environment links
INSERT INTO disease_environment (disease_id, condition_value_id, weight)
SELECT d.id, ecv.id, x.weight
FROM (
    VALUES
        ('Early Blight', 'Humidity', 'High', 3),
        ('Early Blight', 'Temperature', 'Warm', 2),
        ('Early Blight', 'Plant spacing', 'Dense', 2),
        ('Late Blight', 'Humidity', 'High', 3),
        ('Late Blight', 'Temperature', 'Cool', 3),
        ('Late Blight', 'Rainfall', 'High', 3),
        ('Septoria Leaf Spot', 'Humidity', 'Moderate', 2),
        ('Septoria Leaf Spot', 'Rainfall', 'Moderate', 2),
        ('Powdery Mildew', 'Humidity', 'Low', 2),
        ('Powdery Mildew', 'Temperature', 'Warm', 2),
        ('Powdery Mildew', 'Plant spacing', 'Dense', 3),
        ('Bacterial Spot', 'Humidity', 'High', 2),
        ('Bacterial Spot', 'Temperature', 'Warm', 2),
        ('Bacterial Spot', 'Rainfall', 'High', 2),
        ('Tomato Mosaic Virus', 'Plant spacing', 'Dense', 1),
        ('Fusarium Wilt', 'Temperature', 'Warm', 3),
        ('Fusarium Wilt', 'Soil moisture', 'Waterlogged', 2),
        ('Blossom End Rot', 'Soil moisture', 'Dry', 2),
        ('Blossom End Rot', 'Soil moisture', 'Waterlogged', 2)
) AS x(disease_name, condition_name, value_name, weight)
JOIN disease d ON d.name = x.disease_name
JOIN environmental_condition ec ON ec.name = x.condition_name
JOIN environmental_condition_value ecv ON ecv.condition_id = ec.id AND ecv.value_name = x.value_name
ON CONFLICT (disease_id, condition_value_id) DO NOTHING;

-- Disease-treatment links
INSERT INTO disease_treatment (disease_id, treatment_id, priority_level)
SELECT d.id, t.id, x.priority_level
FROM (
    VALUES
        ('Early Blight', 'Remove infected leaves', 1),
        ('Early Blight', 'Apply chlorothalonil fungicide', 2),
        ('Early Blight', 'Improve plant spacing', 3),
        ('Late Blight', 'Remove infected leaves', 1),
        ('Late Blight', 'Apply copper-based fungicide', 2),
        ('Late Blight', 'Isolate infected plants', 3),
        ('Septoria Leaf Spot', 'Remove infected leaves', 1),
        ('Septoria Leaf Spot', 'Apply chlorothalonil fungicide', 2),
        ('Septoria Leaf Spot', 'Reduce overhead irrigation', 3),
        ('Powdery Mildew', 'Apply chlorothalonil fungicide', 1),
        ('Powdery Mildew', 'Improve plant spacing', 2),
        ('Powdery Mildew', 'Remove infected leaves', 3),
        ('Bacterial Spot', 'Apply copper-based fungicide', 1),
        ('Bacterial Spot', 'Reduce overhead irrigation', 2),
        ('Bacterial Spot', 'Sanitize tools and stakes', 3),
        ('Tomato Mosaic Virus', 'Remove infected leaves', 1),
        ('Tomato Mosaic Virus', 'Isolate infected plants', 2),
        ('Tomato Mosaic Virus', 'Use disease-resistant varieties', 3),
        ('Fusarium Wilt', 'Soil drench with approved fungicide', 1),
        ('Fusarium Wilt', 'Use disease-resistant varieties', 2),
        ('Fusarium Wilt', 'Isolate infected plants', 3),
        ('Blossom End Rot', 'Apply calcium foliar spray', 1),
        ('Blossom End Rot', 'Reduce overhead irrigation', 2)
) AS x(disease_name, treatment_name, priority_level)
JOIN disease d ON d.name = x.disease_name
JOIN treatment t ON t.name = x.treatment_name
ON CONFLICT (disease_id, treatment_id) DO NOTHING;
