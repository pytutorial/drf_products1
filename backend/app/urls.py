from django.urls import path

from . import views

urlpatterns = [
    path('products', views.getProducts),
    path('product/<int:id>', views.getProduct),
    path('create_product', views.createProduct),
    path('update_product/<int:id>', views.updateProduct),
    path('delete_product/<int:id>', views.deleteProduct)
]