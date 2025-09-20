from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('id', 'name', 'price', 'category')
    list_filter = ('name', 'price', 'category')
    ordering = ['id', 'name']

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')
    ordering = ['id', 'name']

admin.site.register(Category, CategoryAdmin)