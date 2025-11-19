from flask import request, abort
from service import app
from service.models import Product, Category
from service.common import status
from service.common import log_handlers

######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    app.logger.info("Request to Retrieve a product with id [%s]", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return product.serialize(), status.HTTP_200_OK

######################################################################
# UPDATE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    app.logger.info("Request to Update a product with id [%s]", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK

######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    app.logger.info("Request to Delete a product with id [%s]", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT

######################################################################
# LIST PRODUCTS + FILTERING
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    app.logger.info("Request to list Products...")
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        category_val = getattr(Category, category.upper())
        products = Product.find_by_category(category_val)
    elif available:
        available_val = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_val)
    else:
        products = Product.all()

    results = [p.serialize() for p in products]
    return results, status.HTTP_200_OK
