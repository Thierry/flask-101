# wsgi.py
from flask import Flask, jsonify
app = Flask(__name__)

PRODUCTS = [
    { 'id': 1, 'name': 'Skello' },
    { 'id': 2, 'name': 'Socialive.tv' },
    { 'id': 3, 'name': 'IDontKnow' }
]

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def get_products():
    return jsonify(PRODUCTS)

@app.route('/api/v1/products/<product_id>')
def get_product_by_id(product_id):
    for product in PRODUCTS:
        if product['id'] == int(product_id):
            return jsonify(product)
    return jsonify({ "error": "id not found" }), 404
