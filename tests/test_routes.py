import os
import logging
from unittest import TestCase
from service import app
from service.models import db
from tests.factories import ProductFactory
from urllib.parse import quote_plus
from service.common import status

BASE_URL = "/products"

class TestProductRoutes(TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_products(self, count):
        products = []
        for _ in range(count):
            product = ProductFactory()
            response = self.client.post(BASE_URL, json=product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_product = response.get_json()
            products.append(ProductFactory(**new_product))
        return products

    def get_product_count(self):
        return len(self.client.get(BASE_URL).get_json())

    def test_get_product(self):
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        new_product = response.get_json()

        new_product["description"] = "unknown"
        response = self.client.put(
            f"{BASE_URL}/{new_product['id']}", json=new_product
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated = response.get_json()
        self.assertEqual(updated["description"], "unknown")

    def test_delete_product(self):
        products = self._create_products(5)
        product_count = self.get_product_count()
        test_product = products[0]

        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_list(self):
        self._create_products(5)
        response = self.client.get(BASE_URL)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_query_by_name(self):
        products = self._create_products(5)
        test_name = products[0].name

        name_count = len([p for p in products if p.name == test_name])

        response = self.client.get(BASE_URL, query_string=f"name={quote_plus(test_name)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)

    def test_query_by_category(self):
        products = self._create_products(10)
        category = products[0].category

        count = len([p for p in products if p.category == category])

        response = self.client.get(
            BASE_URL, query_string=f"category={category.name}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(len(data), count)

    def test_query_by_availability(self):
        products = self._create_products(10)

        available_count = len([p for p in products if p.available])

        response = self.client.get(BASE_URL, query_string="available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), available_count)
