from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status
import os
from django.core.files.storage import FileSystemStorage

from .models import Product
from .serializers import ProductSerializer

fs = FileSystemStorage()
IMG_DIR = os.path.join('static', 'product_images')
IMG_URL_PREFIX = 'http://localhost:8000/static/product_images/'

def saveImage(image):
    imgPath = os.path.join(IMG_DIR, image.name)
    savedPath = fs.save(imgPath, image)
    fileName = os.path.basename(savedPath)
    return IMG_URL_PREFIX + fileName

def deleteImage(imageURL):
    fileName = imageURL.split('/')[-1]
    filePath = os.path.join(IMG_DIR, fileName)
    
    if os.path.exists(filePath):
        os.remove(filePath)

@api_view(['GET'])
def getProduct(request, id):
    product = Product.objects.get(pk=id)
    return Response(ProductSerializer(product).data)

@api_view(['GET'])
def getProducts(request):    
   products = Product.objects.all()
   return Response([
       ProductSerializer(prod).data for prod in products
   ])

@api_view(['POST'])
def createProduct(request):
    errors = {}
    data = {key : values for (key, values) in request.data.items()}
    image = request.FILES.get('image')
    imageURL = None
    
    if image == None or image.name == '':
        errors['image'] = 'Product image required.'
    else:
        imageURL = data['imageURL'] = saveImage(image)    
    
    serializer = ProductSerializer(data=data)
    valid = serializer.is_valid()
    param_errors = {param : str(serializer.errors[param][0]) for param in serializer.errors}
    errors.update(param_errors)

    if len(errors) > 0 :
        if imageURL:
            deleteImage(imageURL)

        return Response({'errors' : errors, 'success' : False })
    
    product = serializer.save()
    return Response({'product' : ProductSerializer(product).data, 'success' : True})

@api_view(['PUT'])
def updateProduct(request, id):
    data = {key : values for (key, values) in request.data.items()}
    product = Product.objects.get(pk=id)

    image = request.FILES.get('image')
    imageURL = None

    if image and image.name:        
        imageURL = data['imageURL'] = saveImage(image)        
    else:
        data['imageURL'] = product.imageURL

    serializer = ProductSerializer(product, data=data)

    if not serializer.is_valid():
        if imageURL:
            deleteImage(imageURL)

        param_errors = {param : str(serializer.errors[param][0]) for param in serializer.errors}
        return Response({ 'errors': param_errors, 'success' : False })
    
    if imageURL and product.imageURL:
        deleteImage(product.imageURL)

    product = serializer.save()

    return Response({'product' : ProductSerializer(product).data, 'success' : True})

@api_view(['DELETE'])
def deleteProduct(request, id):
    product = Product.objects.get(pk=id)
    
    if product.imageURL:
        deleteImage(product.imageURL)
        
    product.delete()
    return Response({'success' : True})
