from django.urls import path
from .views import ListItemsAPIView, ItemRetrieveUpdateDestroyAPIView, CategoryAPIView, EcommerceExcelReport, CreateItemAPIView

urlpatterns = [
    # List item instances
    path('gallery', ListItemsAPIView.as_view(), name='gallery'),
    # Retrieve, update & delete item instances
    path('gallery/<int:id>', ItemRetrieveUpdateDestroyAPIView.as_view(), name='gallery'),
    # Create item instances
    path('gallery-create', CreateItemAPIView.as_view(), name='gallery'),
    # Create & list category instances
    path('categories', CategoryAPIView.as_view(), name='categories'),
    # Generate excel report
    path('ecommerce-report', EcommerceExcelReport, name='report'),
]