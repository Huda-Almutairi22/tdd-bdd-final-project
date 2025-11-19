import requests
from behave import given
from service.common.status import HTTP_201_CREATED

@given('the following products')
def step_impl(context):
    rest_endpoint = context.base_url + "/products"

    # delete all existing products
    requests.delete(rest_endpoint)

    # load new products
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"] in ["True", "true", "1"],
            "category": row["category"]
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED
