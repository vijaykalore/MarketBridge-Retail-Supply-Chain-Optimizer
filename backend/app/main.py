from flask import Flask, render_template, request, jsonify, abort
import os

from . import models, crud, predictor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'db.sqlite'))

# initialize sqlite tables if needed
models.init_db(DB_PATH)

static_dir = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, '..', 'templates'), static_folder=static_dir)

@app.route('/')
def home():
    inv = crud.get_inventory(DB_PATH)
    products = crud.get_products(DB_PATH)
    return render_template('index.html', inventory=inv, products=products)

@app.route('/api/inventory', methods=['GET'])
def api_inventory():
    items = crud.get_inventory(DB_PATH)
    return jsonify(items)


@app.route('/api/products', methods=['GET'])
def api_products():
    prods = crud.get_products(DB_PATH)
    return jsonify(prods)

@app.route('/api/inventory', methods=['POST'])
def api_create_inventory():
    data = request.get_json()
    if not data:
        abort(400)
    # ensure product exists
    prods = crud.get_products(DB_PATH)
    if not any(p['id'] == data.get('product_id') for p in prods):
        abort(400, 'Product not found')
    created = crud.create_inventory(DB_PATH, data)
    return jsonify(created), 201

@app.route('/api/product', methods=['POST'])
def api_create_product():
    data = request.get_json()
    if not data:
        abort(400)
    created = crud.create_product(DB_PATH, data)
    return jsonify(created), 201

@app.route('/api/predict/<int:product_id>', methods=['GET'])
def api_predict(product_id):
    inv = crud.get_inventory_by_product(DB_PATH, product_id)
    if not inv:
        return jsonify({'product_id': product_id, 'recommended_restock': 10, 'reason': 'no inventory records, default safety stock'})
    # inventory rows are dictionaries from sqlite helper
    recent = [i['quantity'] for i in inv]
    need = predictor.predict_restock_quantities(recent, safety_stock=10)
    return jsonify({'product_id': product_id, 'recommended_restock': need, 'recent': recent})

if __name__ == '__main__':
    app.run(debug=True)
