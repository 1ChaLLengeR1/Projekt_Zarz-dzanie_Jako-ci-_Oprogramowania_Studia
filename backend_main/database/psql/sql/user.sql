INSERT INTO users (id, username, email, password, is_active)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'admin',
    'admin@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$FqazG2AMLrB/XpC3f+ggcQ$LibJfI1GIUHD7WxeMLFWXGAW3CDQ6P9XTm1MKufWWZ8',
    true
)
ON CONFLICT (id) DO NOTHING;