# tests/test_views.py
from flask_testing import TestCase
import json
from wsgi import app

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_valid_product(self):
        response = self.client.get("/api/v1/products/1")
        self.assertEqual(response.status, "200 OK")
        product = response.json
        self.assertIsInstance(product, dict)
        self.assertEqual(product, { 'id': 1, 'name': 'Skello' })

    def test_unknown_product(self):
        response = self.client.get("/api/v1/products/17")
        self.assertEqual(response.status, "404 NOT FOUND")

    def test_create_product(self):
        new_product = { 'name': 'My New Product' }
        response = self.client.post("/api/v1/products", data=json.dumps(new_product), content_type='application/json')
        self.assertEqual(response.status, "201 CREATED")
        product = response.json
        self.assertIsInstance(product, dict)
        id = product['id']

        response = self.client.get(f"/api/v1/products/{id}")
        self.assertEqual(response.status, "200 OK")
        product = response.json
        self.assertIsInstance(product, dict)
        self.assertEqual(product, { 'id': id, 'name': 'My New Product' })


# test_zz_* to run last
    def test_zz_delete_unknown_product(self):
        response = self.client.delete("/api/v1/products/17")
        self.assertEqual(response.status, "404 NOT FOUND")

    def test_zz_delete_valid_product(self):
        response = self.client.delete("/api/v1/products/1")
        self.assertEqual(response.status, "204 NO CONTENT")
        response = self.client.get("/api/v1/products/1")
        self.assertEqual(response.status, "404 NOT FOUND")
