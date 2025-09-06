import os
import sys

# ensure app package can be found
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest
from app.main import app


@pytest.fixture
def client():
    with app.test_client() as c:
        yield c


def test_root_and_inventory_empty(client):
    r = client.get('/')
    assert r.status_code == 200
    r = client.get('/api/inventory')
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


def test_create_product_and_inventory_and_predict(client):
    prod = {"name": "Test Product", "sku": "TP-001", "category": "General"}
    r = client.post('/api/product', json=prod)
    assert r.status_code == 201
    created = r.get_json()
    pid = created['id']

    inv = {"product_id": pid, "location_id": "WH-1", "quantity": 5}
    r = client.post('/api/inventory', json=inv)
    assert r.status_code == 201

    r = client.get(f'/api/predict/{pid}')
    assert r.status_code == 200
    data = r.get_json()
    assert 'recommended_restock' in data
