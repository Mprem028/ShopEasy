import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ecommerce.settings')
django.setup()
from accounts.models import CustomUser
from products.models import Product

ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL','admin@example.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD','Admin@12345')

def create_admin():
    if not CustomUser.objects.filter(email=ADMIN_EMAIL).exists():
        admin = CustomUser.objects.create_user(username='admin', email=ADMIN_EMAIL, password=ADMIN_PASSWORD, role='admin', is_staff=True)
        print("Created admin:", ADMIN_EMAIL)
    else:
        print("Admin exists")

def create_products():
    samples = [
        {"name":"Blue T-Shirt","price":499.00,"stock":50,"category":"Apparel","description":"Comfortable cotton tee."},
        {"name":"Running Shoes","price":2999.00,"stock":20,"category":"Footwear","description":"Lightweight running shoes."},
        {"name":"Wireless Earbuds","price":1499.00,"stock":35,"category":"Electronics","description":"Noise cancelling earbuds."},
    ]
    for s in samples:
        if not Product.objects.filter(name=s['name']).exists():
            p = Product.objects.create(name=s['name'], price=s['price'], stock=s['stock'], category=s['category'], description=s['description'])
            print("Created", p.name)

if __name__ == '__main__':
    create_admin()
    create_products()
