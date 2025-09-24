from helpers.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from django.http import HttpResponse
# 
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, CreateProductSerializer
from helpers.functions import create_excel_table, bar, line, pie, histogram
from helpers.styles import DEFAULT_STYLE_DIC

# Create your views here.

class ListItemsAPIView(ListCreateAPIView):
    # Define serializer class
    serializer_class = ProductSerializer
    
    # Pagination class
    pagination_class = CustomPageNumberPagination

    # Filters
    filter_backends = [DjangoFilterBackend,
                    filters.SearchFilter, filters.OrderingFilter]
    
    permission_classes = [IsAuthenticated]
    
    filterset_fields = ['id', 'name', 'price', 'category']
    
    search_fields = ['id', 'name', 'price', 'category']
    
    ordering_fields = ['id', 'name', 'price']

    # Retrieve all items
    def get_queryset(self):
        return Product.objects.filter()

class CreateItemAPIView(CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateProductSerializer

class ItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # Define serializer class
    serializer_class = CreateProductSerializer

    # Define look up field
    lookup_field = "id"

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs['id'])

class CategoryAPIView(ListCreateAPIView):
    # Define serializer class
    serializer_class = CategorySerializer
    
    # Pagination class
    pagination_class = CustomPageNumberPagination

    # Filters
    filter_backends = [DjangoFilterBackend,
                    filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id', 'name']
    
    search_fields = ['id', 'name']
    
    ordering_fields = ['id', 'name']

    # Save bias
    def perform_create(self, serializer):
        return serializer.save()

    # Retrieve all categories
    def get_queryset(self):
        return Category.objects.filter()

def EcommerceExcelReport(request):
    # Create new excel worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Excel stadistics report"  # worksheet name

    items = Product.objects.all()

    most_expensive_items = items.order_by('-price')[:10]

    x_headers = [f"Item - {item.pk}" for item in most_expensive_items]
    graph_values = [int(item.price) for item in most_expensive_items]

    PROPERTIES = {
            'labels': x_headers,
            'graph_values': graph_values,
            'colors': ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:purple', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'],
            'y_title': 'Decreasing values',
            'x_title': 'Item id axis',
            'main_title': 'Most expensive gallery',
            'position': 'B2',
            'linestyle': 'solid',
            'legend': True,
            'facecolor': '#d0d3d4',
            'background': '#f0f0f0',
            'figsize': (10,4),
            'legend_title': 'Item list',
            'edgecolor': 'black'
        }

    bar(ws, PROPERTIES)

    PROPERTIES.update({'position': 'B24', 'marker': 'o', 'linestyle': '-', 'color': 'black'})

    line(ws, PROPERTIES)

    PROPERTIES.update({'position': 'AE2',
                       'font': 'Courier New',
                        'weight': 'light',
                        'size': 10
                       })

    PROPERTIES.pop('y_title')
    PROPERTIES.pop('x_title')
    pie(ws, PROPERTIES)

    cheapest_items = items.order_by('price')[:10]
    x_headers = [f"Item - {item.pk}" for item in cheapest_items]
    cheapest_items = [int(item.price) for item in cheapest_items]

    PROPERTIES.update({'position': 'P2', 'labels': x_headers, 'graph_values': cheapest_items,
                    'main_title': 'Cheapest gallery', 'y_title': 'Increasing values ', })
    
    bar(ws, PROPERTIES)

    PROPERTIES.update({'position': 'O24'})

    line(ws, PROPERTIES)

    PROPERTIES.update({'position': 'AB29'})

    PROPERTIES.pop('y_title')
    pie(ws, PROPERTIES)

    category_ids = list(Category.objects.values_list('id', flat=True))
    id_histogram_list = []

    for i in category_ids:
        count = Product.objects.filter(category__id=i).count()
        for u in range(count):
            id_histogram_list.append(i)

    PROPERTIES.update({'graph_values': id_histogram_list, 'position': 'B46', 'font_size': 10, 'color': 'blue', 'figsize': (10,4)})

    histogram(ws, PROPERTIES)

    # Second worksheet
    tables_sheet = wb.create_sheet(title="Data")

    # Create table data
    main_data = {'Product': [], 'Description': [], 'Price': [], 'Category': []}

    for item in items:
        main_data['Product'].append(item.name)
        main_data['Description'].append(item.description)
        main_data['Price'].append(item.price)
        main_data['Category'].append(item.category.name)
    create_excel_table(tables_sheet, main_data, DEFAULT_STYLE_DIC, (2, 2))

    # Prepare your response as a .xlsx file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_estadisticas.xlsx'

    wb.save(response)
    return response
