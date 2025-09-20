from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from helpers.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
# 
from helpers.functions import create_excel_table, bar, line, scatter, pie
from helpers.styles import DEFAULT_STYLE_DIC
from openpyxl import Workbook
from django.http import HttpResponse
# Create your views here.

class ItemAPIView(ListCreateAPIView):
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

    # Save bias
    def perform_create(self, serializer):
        return serializer.save()

    # Retrieve all items
    def get_queryset(self):
        return Product.objects.filter()

class ItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # Define serializer class
    serializer_class = ProductSerializer

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

    # Second worksheet
    tables_sheet = wb.create_sheet(title="Data")

    items = Product.objects.all()

    most_expensive_items = items.order_by('-price')[:10]

    x_headers = [f"Item - {item.pk}" for item in most_expensive_items]
    most_expensive_items = [int(item.price) for item in most_expensive_items]

    PROPERTIES = {
            'labels': x_headers,
            'graph_values': most_expensive_items,
            'colors': ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:purple', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'],
            'y_title': 'Ordered comparative',
            'x_title': 'Item axis',
            'main_title': 'The most expensive gallery items',
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

    cheapest_items = items.order_by('price')[:10]
    x_headers = [f"Item - {item.pk}" for item in cheapest_items]
    cheapest_items = [int(item.price) for item in cheapest_items]

    PROPERTIES.update({'position': 'B24', 'labels': x_headers, 'graph_values': cheapest_items,
                    'main_title': 'The cheapest gallery items', 'y_title': 'Cheapest items', })
    
    bar(ws, PROPERTIES)

    # PROPERTIES.update({'position': 'B24', 'labels': country_names, 'graph_values': population_values,
    #                 'main_title': 'Population countries', 'y_title': 'Population', 'x_title': 'Countries'})
    
    # bar(ws, PROPERTIES)

    # PROPERTIES.pop('y_title')
    # PROPERTIES.pop('x_title')

    # PROPERTIES.update({'position': 'Q2',
    #                    'legend_title': 'Area distribution',
    #                    'color': 'black',
    #                    'font': 'Courier New',
    #                     'weight': 'light',
    #                     'size': 10
    #                    })

    # pie(ws, PROPERTIES)

    # population_values = total_country_list.order_by('-population')[:10]
    # country_names = [country.name for country in population_values]
    # population_values = [country.population for country in population_values]

    # PROPERTIES.pop('y_title')
    # PROPERTIES.pop('x_title')

    # PROPERTIES.update({'position': 'Q28'})

    # pie(ws, PROPERTIES)

    # # Lineal graphics

    # longest_longitudes = total_country_list.order_by('-longitude')[:10]
    # long_values = [country.longitude for country in longest_longitudes]
    # long_names = [country.name for country in longest_longitudes]

    # longest_latitudes = total_country_list.order_by('-latitude')[:10]
    # lat_values = [country.latitude for country in longest_latitudes]
    # lat_names = [country.name for country in longest_latitudes]

    # PROPERTIES.update({'position': 'Z2', 'x_title': 'Countries', 'y_title': 'longitudes', 'main_title': 'Greatest longitudes',
    #                 'graph_values': long_values, 'labels': long_names, 'figsize': (10, 4), 'marker': 'o', 'linestyle': '-'})

    # line(ws, PROPERTIES)

    # PROPERTIES.update({'position': 'Z28', 'x_title': 'Countries', 'y_title': 'latitudes', 'main_title': 'Greates latitudes',
    #                 'graph_values': lat_values, 'labels': lat_names, 'figsize': (10, 4)})

    # line(ws, PROPERTIES)

    # Prepare your response as a .xlsx file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_estadisticas.xlsx'

    wb.save(response)
    return response
