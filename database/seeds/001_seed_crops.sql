-- Seed crops (recommended: Tomato)

INSERT INTO crop (name, description) VALUES
    ('Tomato', 'Solanum lycopersicum — primary crop for this expert system demo.')
ON CONFLICT (name) DO NOTHING;
