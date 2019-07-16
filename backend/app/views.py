from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def getProducts(request):    
   products = Product.objects.all()
   return Response([
       ProductSerializer(prod).data for prod in products
   ])