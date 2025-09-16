import sqlite3
from sqlite3 import Connection
from typing import List, Dict, Any
import os

DB_PATH = os.getenv('CHATBOT_DB', 'chatbot.db')

def get_conn() -> Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(open('models.sql').read())
    conn.commit()
    conn.close()

def save_message(user_id: str, role: str, content: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO messages (user_id, role, content) VALUES (?,?,?)', (user_id, role, content))
    conn.commit()
    conn.close()

def get_last_n_messages(user_id: str, n: int = 3) -> List[Dict[str, str]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT role, content, created_at FROM messages WHERE user_id=? ORDER BY id DESC LIMIT ?', (user_id, n))
    rows = cur.fetchall()
    conn.close()
    messages = [dict(r) for r in rows][::-1]
    return messages

def save_order_example():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as c FROM orders WHERE id=1001')
    if cur.fetchone()['c'] == 0:
        cur.execute('INSERT INTO orders (id, user_id, status, shipping_provider, eta) VALUES (?,?,?,?,?)',
                    (1001, 'u123', 'Shipped', 'JNE', '2025-09-18'))
        conn.commit()
    conn.close()

def get_order_by_id(order_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE id=?', (order_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)

def save_products_example():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as c FROM products')
    if cur.fetchone()['c'] == 0:
        products = [
            ('LaptopA', 'Laptop entry-level dengan RAM 8GB dan SSD 256GB.'),
            ('SmartphoneX', 'Smartphone dengan kamera 108MP dan baterai tahan lama.'),
            ('HeadsetZ', 'Headset gaming dengan surround sound dan mikrofon noise-cancelling.')
        ]
        cur.executemany('INSERT INTO products (name, description) VALUES (?,?)', products)
        conn.commit()
    conn.close()

def get_product_by_name(name: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE lower(name)=lower(?)', (name,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)