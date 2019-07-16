# python manage.py migrate
# python manage.py shell 
# Copy --> shell

from app.models import Product

Product.objects.create(
    code = '0001',
    name = 'Product 1',
    description = 'Product 1 detail',
    unitPrice = 10000,
    imageURL = 'https://keyassets-p2.timeincuk.net/wp/prod/wp-content/uploads/sites/53/2018/04/pick-and-mix-chocolate-and-sweet-cake.jpg'
)