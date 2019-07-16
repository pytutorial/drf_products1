from rest_framework.serializers import ModelSerializer
from .models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('code', 'name', 'description',
                    'unitPrice', 'imageURL')