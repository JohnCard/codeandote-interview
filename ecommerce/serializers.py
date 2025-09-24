from rest_framework.serializers import ModelSerializer
from .models import Product, Category
from django.forms.models import model_to_dict

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]

class ProductSerializer(ModelSerializer):

    # Foreign relationships
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image']

class CreateProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']