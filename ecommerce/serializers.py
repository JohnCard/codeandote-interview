from rest_framework.serializers import ModelSerializer
from .models import Product, Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]

class ProductSerializer(ModelSerializer):

    # Foreign relationships
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "category", "image"]
        read_only_fields = ['category']