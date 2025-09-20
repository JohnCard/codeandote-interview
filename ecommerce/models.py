from django.db import models
from helpers.models import TrackingModel, BasicModel
from helpers.functions import random_index, random_decimal, random_image

# Create your models here.

class Category(TrackingModel, BasicModel):
    def __str__(self):
        return self.name

class Product(TrackingModel, BasicModel):
    # Item price
    price = models.DecimalField(verbose_name="Item value", blank=True, null=True, decimal_places=2, max_digits=9)
    # Item image
    image = models.ImageField(null=True, blank=True, upload_to='img')
    # Item category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.name