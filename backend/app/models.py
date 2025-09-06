import sqlite3
import datetime
from typing import List, Dict, Any


def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT,
            category TEXT,
            supplier_id INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            location_id TEXT NOT NULL,
            quantity INTEGER DEFAULT 0,
            last_updated TEXT
        )
    ''')
    conn.commit()
    conn.close()


def dict_from_row(row, cols):
    return {k: row[idx] for idx, k in enumerate(cols)}

