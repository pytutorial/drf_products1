from django.db import models

class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(blank=True, max_length=200)
    unitPrice = models.FloatField(db_column='unit_price')
    imageURL = models.CharField(db_column='image_url', blank=True, max_length=1024)