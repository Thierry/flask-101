# wsgi.py
from flask import Flask, jsonify, request
app = Flask(__name__)

PRODUCTS = [
    { 'id': 1, 'name': 'Skello' },
    { 'id': 2, 'name': 'Socialive.tv' },
    { 'id': 3, 'name': 'IDontKnow' }
]

def get_new_id():
    cpt = 0
    for product in PRODUCTS:
        if product['id'] >= cpt:
            cpt = product['id'] + 1
    return cpt

def get_product(id):
    if type(id) == str:
        id = int(id)
    for product in PRODUCTS:
        if product['id'] == id:
            return product
    return None

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def get_products():
    return jsonify(PRODUCTS)

@app.route('/api/v1/products', methods = [ 'POST' ])
def create_product():
    product = request.get_json()
    if product is None:
        return "", 400
    product['id'] = get_new_id()
    PRODUCTS.append(product)
    return jsonify(product), 201

@app.route('/api/v1/products/<product_id>')
def get_product_by_id(product_id):
    product = get_product(product_id)
    if product != None:
        return jsonify(product)
    return jsonify({ "error": "id not found" }), 404

@app.route('/api/v1/products/<product_id>', methods = ['DELETE'])
def delete_product_by_id(product_id):
    for index, product in enumerate(PRODUCTS):
        if product['id'] == int(product_id):
            del PRODUCTS[index]
            return "", 204
    return "",404
