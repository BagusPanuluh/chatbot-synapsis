CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    status TEXT,
    shipping_provider TEXT,
    eta TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);


-- Seed example order
INSERT OR IGNORE INTO orders (id, user_id, status, shipping_provider, eta)
VALUES (1001, 'u123', 'Shipped', 'JNE', '2025-09-18');

-- Table products
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT
);

-- Seed example products
INSERT OR IGNORE INTO products (name, description) VALUES
  ('LaptopX', 'Laptop entry-level dengan RAM 8GB dan SSD 256GB.'),
  ('SmartphoneY', 'Smartphone dengan kamera 108MP dan baterai tahan lama.'),
  ('HeadsetZ', 'Headset gaming dengan surround sound dan mikrofon noise-cancelling.');