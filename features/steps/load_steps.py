# محو المحتوى القديم وإنشاء ملف Python نظيف
$pythonCode = @'
"""
Load Steps for Behave
"""
from behave import given
from service.models import Product

@given('the following products')
def step_impl(context):
    """Delete all products and load new ones"""
    # First, delete all existing products to start fresh
    Product.query.delete()
    
    # Create products from the feature table
    for row in context.table:
        product = Product()
        product.name = row['name']
        product.description = row['description']
        product.price = float(row['price'])
        product.category = row['category']
        product.available = row['available'].lower() in ['true', 'yes', '1']
        product.create()
'@

# حفظ الملف بشكل صحيح
$pythonCode | Out-File -FilePath features/steps/load_steps.py -Encoding utf8 -NoNewline