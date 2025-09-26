from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from django.http import HttpResponse
# 
from helpers.pagination import CustomPageNumberPagination
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, CreateProductSerializer
from helpers.functions import create_excel_table, bar, line, pie, histogram
from helpers.styles import DEFAULT_STYLE_DIC
from .filters import ProductFilter
# Create your views here.

class ListItemsAPIView(ListAPIView):
    # Define serializer class
    serializer_class = ProductSerializer

    # Pagination class
    pagination_class = CustomPageNumberPagination

    filterset_class = ProductFilter

    permission_classes = [IsAuthenticated]

    # Retrieve all items
    queryset = Product.objects.all()

class ListFilterItems(ListAPIView):
    # Define serializer class
    serializer_class = ProductSerializer
    
    # Pagination class
    pagination_class = CustomPageNumberPagination

    # Filters
    filter_backends = [DjangoFilterBackend,
                    filters.SearchFilter, filters.OrderingFilter]

    permission_classes = [IsAuthenticated]
    
    filterset_fields = ['id', 'name', 'price', 'category', 'category__name']

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

class CategoryAPIView(ListAPIView):
    # Define serializer class
    serializer_class = CategorySerializer
    # Pagination class
    pagination_class = CustomPageNumberPagination
    queryset = Category.objects.all()

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
        'figsize': (10,4),
        'labels': x_headers,
        'graph_values': graph_values,
        'colors': ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:purple', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'],
        'y_title': 'Decreasing values',
        'x_title': 'Item id axis',
        'main_title': 'Most expensive gallery',
        'position': 'B2',
        'legend': True,
        'facecolor': '#15A9AB',
        'background': '#1290A6',
        'legend_title': 'Item list',
        'edgecolor': 'black',
        'bbox_to_anchor': (1.3, 0.8),
        'font_size': 9,
        'ha': 'center',
        'fontweight': 'bold',
        'border_linewidth': 3,
        'border_color': 'black',
        'margins_y': 0.2
        }

    bar(ws, PROPERTIES)

    PROPERTIES.update({'position': 'B23', 'marker': 'o', 'linestyle': '-', 'plot_color': 'black', 'linewidth': 0.5, 'font_size': 10, 'color': 'black', 'plot_text_color': 'yellow'})

    line(ws, PROPERTIES)

    PROPERTIES.pop('y_title')
    PROPERTIES.pop('x_title')

    PROPERTIES.update({'position': 'AH2',
                        'font': 'Courier New',
                        'weight': 'light',
                        'size': 11,
                        'shadow': True,
                        'bbox_to_anchor': (1.2,.8),
                        'autopct': '%1.1f%%'
                        })

    pie(ws, PROPERTIES)

    cheapest_items = items.order_by('price')[:10]
    x_headers = [f"Item - {item.pk}" for item in cheapest_items]
    cheapest_items = [int(item.price) for item in cheapest_items]

    PROPERTIES.update({'position': 'R2', 'labels': x_headers, 'graph_values': cheapest_items,
                    'main_title': 'Cheapest gallery', 'y_title': 'Increasing values', 'bbox_to_anchor': (1.3, 0.8)})

    bar(ws, PROPERTIES)

    PROPERTIES.update({'position': 'O23', 'font_size': 10})

    line(ws, PROPERTIES)

    PROPERTIES.pop('y_title')

    PROPERTIES.update({'position': 'AB24',
                    'bbox_to_anchor': (1.2,.8)})

    pie(ws, PROPERTIES)

    category_ids = list(Category.objects.values_list('id', flat=True))
    id_histogram_list = []

    for i in category_ids:
        count = Product.objects.filter(category__id=i).count()
        for u in range(count):
            id_histogram_list.append(i)

    PROPERTIES.update({'graph_values': id_histogram_list, 'position': 'B44', 'font_size': 10, 'color': 'blue', 'figsize': (10,4), 'linestyle': '--'})

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
