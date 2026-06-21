-- Seed roles and default accounts
-- Default passwords: admin123 / farmer123 / expert123 (SHA-256 hashes)

INSERT INTO role (code, label) VALUES
    ('admin', 'System Administrator'),
    ('farmer', 'Farmer')
ON CONFLICT (code) DO NOTHING;

INSERT INTO farmer (full_name, phone_number, location, email)
SELECT 'Demo Farmer', '670000000', 'Buea', 'farmer@demo.local'
WHERE NOT EXISTS (SELECT 1 FROM farmer WHERE email = 'farmer@demo.local');

INSERT INTO app_user (username, password_hash, role_id, farmer_id, full_name)
SELECT 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
       r.id, NULL, 'System Admin'
FROM role r WHERE r.code = 'admin'
ON CONFLICT (username) DO NOTHING;

INSERT INTO app_user (username, password_hash, role_id, farmer_id, full_name)
SELECT 'farmer1', '26c07fc7be1668f8ea7e3801d4ffdbf33de487a593a69028936ec49f2c89f6ab',
       r.id, f.id, f.full_name
FROM role r
CROSS JOIN farmer f
WHERE r.code = 'farmer' AND f.email = 'farmer@demo.local'
ON CONFLICT (username) DO NOTHING;

INSERT INTO app_user (username, password_hash, role_id, farmer_id, full_name)
SELECT 'expert', '34a6c1a9600377c8dc05ea00380f406fb52e8104e921dc6bd5869bfdf1516164',
       r.id, NULL, 'Crop Expert'
FROM role r WHERE r.code = 'admin'
ON CONFLICT (username) DO NOTHING;
