from django.urls import path
from .views import ItemAPIView, ItemRetrieveUpdateDestroyAPIView, CategoryAPIView, EcommerceExcelReport

urlpatterns = [
    # Create & list item instances
    path('gallery', ItemAPIView.as_view(), name='gallery'),
    # Retrieve, update & delete item instances
    path('gallery/<int:id>', ItemRetrieveUpdateDestroyAPIView.as_view(), name='country'),
    # Create & list category instances
    path('categories', CategoryAPIView.as_view(), name='categories'),
    # Generate excel report
    path('ecommerce-report', EcommerceExcelReport, name='report'),
]