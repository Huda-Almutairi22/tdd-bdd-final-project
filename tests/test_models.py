import unittest
from service.models import Product, db
from tests.factories import ProductFactory

class TestProductModel(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(found.price, product.price)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        product.description = "testing"
        original_id = product.id
        product.update()

        products = Product.all()
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "testing")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products"""
        products = Product.all()
        self.assertEqual(products, [])

        for _ in range(5):
            ProductFactory().create()

        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(5)
        for p in products:
            p.create()

        name = products[0].name
        count = len([p for p in products if p.name == name])

        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for p in found:
            self.assertEqual(p.name, name)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)
        for p in products:
            p.create()

        available = products[0].available
        count = len([p for p in products if p.available == available])

        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for p in found:
            self.assertEqual(p.available, available)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)
        for p in products:
            p.create()

        category = products[0].category
        count = len([p for p in products if p.category == category])

        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for p in found:
            self.assertEqual(p.category, category)
