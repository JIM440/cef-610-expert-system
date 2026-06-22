-- Migration 017: Store crop experts as a first-class database role.

INSERT INTO role (code, label)
VALUES ('expert', 'Crop Expert')
ON CONFLICT (code) DO UPDATE SET label = EXCLUDED.label;

UPDATE app_user
SET role_id = (SELECT id FROM role WHERE code = 'expert')
WHERE username = 'expert';
