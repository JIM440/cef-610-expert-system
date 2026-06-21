-- Seed reusable symptoms (one symptom per row)

INSERT INTO symptom (name, description) VALUES
    ('Brown spots on leaves', 'Circular to irregular brown lesions on foliage'),
    ('Yellowing leaves', 'Chlorosis starting from lower or older leaves'),
    ('Wilting leaves', 'Leaves droop despite adequate soil moisture'),
    ('White powdery coating', 'Powdery white fungal growth on leaf surfaces'),
    ('Dark water-soaked lesions', 'Dark, greasy-looking spots that spread rapidly'),
    ('Leaf curling', 'Upward or downward curling of leaf margins'),
    ('Stunted growth', 'Reduced plant height and fruit development'),
    ('Fruit rot at blossom end', 'Dark sunken area at the bottom of fruit'),
    ('Mosaic leaf pattern', 'Mottled light and dark green leaf discoloration'),
    ('Stem cankers', 'Sunken lesions on stems and petioles'),
    ('Leaf drop', 'Premature shedding of lower leaves'),
    ('Purple leaf veins', 'Purplish discoloration along leaf veins')
ON CONFLICT (name) DO NOTHING;
