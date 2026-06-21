-- Seed treatments (one treatment per row, reused across diseases)

INSERT INTO treatment (name, description) VALUES
    ('Remove infected leaves', 'Prune and destroy affected foliage to reduce pathogen spread'),
    ('Apply copper-based fungicide', 'Spray approved copper fungicide per label instructions'),
    ('Apply chlorothalonil fungicide', 'Broad-spectrum fungicide for fungal leaf diseases'),
    ('Improve plant spacing', 'Increase airflow by thinning or wider row spacing'),
    ('Reduce overhead irrigation', 'Water at soil level to keep foliage dry'),
    ('Apply calcium foliar spray', 'Supplement calcium to reduce blossom end rot risk'),
    ('Soil drench with approved fungicide', 'Target root-zone pathogens with labeled product'),
    ('Use disease-resistant varieties', 'Plant cultivars with known resistance genes'),
    ('Sanitize tools and stakes', 'Disinfect equipment between plants'),
    ('Isolate infected plants', 'Separate symptomatic plants to limit spread')
ON CONFLICT (name) DO NOTHING;
