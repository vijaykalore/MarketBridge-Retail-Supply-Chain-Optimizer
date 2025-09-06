import sqlite3
import datetime
from typing import List, Dict, Any
from . import models


def create_product(db_path: str, product: dict) -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO products (name, sku, category, supplier_id) VALUES (?,?,?,?)',
              (product.get('name'), product.get('sku'), product.get('category'), product.get('supplier_id')))
    conn.commit()
    pid = c.lastrowid
    c.execute('SELECT id, name, sku, category, supplier_id FROM products WHERE id=?', (pid,))
    row = c.fetchone()
    conn.close()
    return {'id': row[0], 'name': row[1], 'sku': row[2], 'category': row[3], 'supplier_id': row[4]}


def get_products(db_path: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, name, sku, category, supplier_id FROM products')
    rows = c.fetchall()
    conn.close()
    return [{'id': r[0], 'name': r[1], 'sku': r[2], 'category': r[3], 'supplier_id': r[4]} for r in rows]


def create_inventory(db_path: str, inv: dict) -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    c.execute('INSERT INTO inventory (product_id, location_id, quantity, last_updated) VALUES (?,?,?,?)',
              (inv.get('product_id'), inv.get('location_id'), inv.get('quantity'), now))
    conn.commit()
    iid = c.lastrowid
    c.execute('SELECT id, product_id, location_id, quantity, last_updated FROM inventory WHERE id=?', (iid,))
    row = c.fetchone()
    conn.close()
    return {'id': row[0], 'product_id': row[1], 'location_id': row[2], 'quantity': row[3], 'last_updated': row[4]}


def get_inventory(db_path: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, product_id, location_id, quantity, last_updated FROM inventory')
    rows = c.fetchall()
    conn.close()
    return [{'id': r[0], 'product_id': r[1], 'location_id': r[2], 'quantity': r[3], 'last_updated': r[4]} for r in rows]


def get_inventory_by_product(db_path: str, product_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, product_id, location_id, quantity, last_updated FROM inventory WHERE product_id=?', (product_id,))
    rows = c.fetchall()
    conn.close()
    return [{'id': r[0], 'product_id': r[1], 'location_id': r[2], 'quantity': r[3], 'last_updated': r[4]} for r in rows]
