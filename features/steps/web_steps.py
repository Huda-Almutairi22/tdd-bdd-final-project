# محتوى features/steps/web_steps.py
@'
"""
Web Steps

Steps file for web interactions with Selenium
"""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

@when('I create a new product with name "{name}", description "{description}", price "{price}", category "{category}", available "{available}"')
def step_impl(context, name, description, price, category, available):
    """Create a new product via REST API"""
    data = {
        "name": name,
        "description": description,
        "price": float(price),
        "category": category,
        "available": available.lower() == "true"
    }
    context.resp = requests.post(f"{context.base_url}/products", json=data)
    assert context.resp.status_code == HTTP_201_CREATED

@when('I request product with id "{product_id}"')
def step_impl(context, product_id):
    """Get a product by ID via REST API"""
    context.resp = requests.get(f"{context.base_url}/products/{product_id}")

@when('I update product "{product_id}" with name "{name}", description "{description}"')
def step_impl(context, product_id, name, description):
    """Update a product via REST API"""
    data = {
        "name": name,
        "description": description
    }
    context.resp = requests.put(f"{context.base_url}/products/{product_id}", json=data)
    assert context.resp.status_code == HTTP_200_OK

@when('I delete product "{product_id}"')
def step_impl(context, product_id):
    """Delete a product via REST API"""
    context.resp = requests.delete(f"{context.base_url}/products/{product_id}")
    assert context.resp.status_code == HTTP_204_NO_CONTENT

@when('I list all products')
def step_impl(context):
    """List all products via REST API"""
    context.resp = requests.get(f"{context.base_url}/products")
    assert context.resp.status_code == HTTP_200_OK

@when('I search for products in category "{category}"')
def step_impl(context, category):
    """Search products by category via REST API"""
    context.resp = requests.get(f"{context.base_url}/products", params={"category": category})
    assert context.resp.status_code == HTTP_200_OK

@when('I search for available products')
def step_impl(context):
    """Search available products via REST API"""
    context.resp = requests.get(f"{context.base_url}/products", params={"available": "true"})
    assert context.resp.status_code == HTTP_200_OK

@when('I search for products named "{name}"')
def step_impl(context, name):
    """Search products by name via REST API"""
    context.resp = requests.get(f"{context.base_url}/products", params={"name": name})
    assert context.resp.status_code == HTTP_200_OK

@then('I should see the product "{name}" in the results')
def step_impl(context, name):
    """Check if product is in results"""
    products = context.resp.json()
    product_names = [p["name"] for p in products]
    assert name in product_names, f"Product {name} not found in {product_names}"

@then('I should get product "{name}"')
def step_impl(context, name):
    """Check if we got the expected product"""
    product = context.resp.json()
    assert product["name"] == name, f"Expected {name}, got {product['name']}"

@then('I should see product "{product_id}" with name "{name}"')
def step_impl(context, product_id, name):
    """Check if product was updated"""
    product = context.resp.json()
    assert product["name"] == name, f"Expected {name}, got {product['name']}"

@then('I should not see product "{name}" in the results')
def step_impl(context, name):
    """Check if product is not in results"""
    products = context.resp.json()
    product_names = [p["name"] for p in products]
    assert name not in product_names, f"Product {name} should not be in {product_names}"

@then('I should see {count:d} products')
def step_impl(context, count):
    """Check the number of products"""
    products = context.resp.json()
    assert len(products) == count, f"Expected {count} products, got {len(products)}"
'@ | Set-Content -FilePath features/steps/web_steps.py -Encoding utf8