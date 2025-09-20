from .models import Country
from .serializers import CountrySerializer
from helpers.pagination import CustomPageNumberPagination
from helpers.functions import create_excel_table, bar, line, scatter, pie, post_new_countries
from helpers.styles import DEFAULT_STYLE_DIC
import requests
from openpyxl import Workbook
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView

# Create your views here.

class CountryAPIView(ListCreateAPIView):
    # Define serializer class
    serializer_class = CountrySerializer
    
    # Pagination class
    pagination_class = CustomPageNumberPagination

    # Filters
    filter_backends = [DjangoFilterBackend,
                    filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['id', 'name', 'region', 'subregion', 'capital']
    
    search_fields = ['id']
    
    ordering_fields = ['id', 'name']

    # Save bias
    def perform_create(self, serializer):
        return serializer.save()

    # Retrieve all orders
    def get_queryset(self):
        return Country.objects.filter()
    
class CountryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer

    # Ask for authentication
    permission_classes = ()

    # Define look up field
    lookup_field = "id"

    def get_queryset(self):
        return Country.objects.filter(id=self.kwargs['id'])

class CreateCountry(GenericAPIView):

    def post(self, request):
        country_name = request.data['country_name']

        url = f'https://restcountries.com/v3.1/name/{country_name}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            Country.objects.create(name=data[0]['name']['common'], region=data[0]['region'], subregion=data[0]['subregion'],
                                capital=data[0].get('capital', ['Desconocida'])[0], population=data[0]['population'],
                                latitude=data[0]['latlng'][0], longitude=data[0]['latlng'][1], area=data[0]['area'],
                                flag=data[0]['flags']['alt'])
            return Response({'ok': True, 'succes': 'New country created'}, status=response.status_code)
        else:
            return Response({'ok': False, 'error': 'Not found data'}, status=response.status_code)

    def put(self, request):
        limit = request.data['limit']
        init = request.data['init']
        status = post_new_countries(init, limit)
        if status == 200:
            return Response({'ok': True, 'succes': 'Countries created'}, status=status)
        else:
            return Response({'ok': False, 'error': 'Not found data'}, status=500)

def excel_report(request):
    # Create new excel worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Final report"  # worksheet name

    # Second worksheet
    ws2 = wb.create_sheet(title="Data")

    total_country_list = Country.objects.all()

    # Create main table
    main_data = {'Country': ['region', 'subregion', 'capital', 'population', 'area', 'latitude', 'longitude']}

    for i in range(0, 100, 9):
        for country in total_country_list[i:i+9]:
            main_data.update({country.name: [country.region, country.subregion, country.capital, country.population, country.area,
                                            country.latitude, country.longitude]})
        create_excel_table(ws2, main_data, DEFAULT_STYLE_DIC, (i+2, 2))
        main_data = {'Country': ['region', 'subregion', 'capital', 'population', 'area', 'latitude', 'longitude']}

    # Bar & pie chart graphs

    greatest_areas = total_country_list.order_by('-area')[:10]
    area_list = [country.area for country in greatest_areas]
    name_list = [country.name for country in greatest_areas]

    PROPERTIES = {
            'labels': name_list,
            'graph_values': area_list,
            'colors': ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:purple'],
            'y_title': 'Area section',
            'x_title': 'Country section',
            'main_title': 'The largest areas',
            'position': 'B2',
            'linestyle': 'solid',
            'legend': True,
            'facecolor': '#d0d3d4',
            'background': '#f0f0f0',
            'figsize': (10,4),
            'legend_title': 'Country list',
            'edgecolor': 'black'
        }

    bar(ws, PROPERTIES)

    PROPERTIES.pop('y_title')
    PROPERTIES.pop('x_title')

    PROPERTIES.update({'position': 'Q2',
                       'legend_title': 'Area distribution',
                       'color': 'black',
                       'font': 'Courier New',
                        'weight': 'light',
                        'size': 10
                       })


    pie(ws, PROPERTIES)

    population_values = total_country_list.order_by('-population')[:10]
    country_names = [country.name for country in population_values]
    population_values = [country.population for country in population_values]

    PROPERTIES.update({'position': 'B24', 'labels': country_names, 'graph_values': population_values,
                    'main_title': 'Population countries', 'y_title': 'Population', 'x_title': 'Countries'})
    
    bar(ws, PROPERTIES)

    PROPERTIES.pop('y_title')
    PROPERTIES.pop('x_title')

    PROPERTIES.update({'position': 'Q28'})

    pie(ws, PROPERTIES)

    # Lineal graphics

    longest_longitudes = total_country_list.order_by('-longitude')[:10]
    long_values = [country.longitude for country in longest_longitudes]
    long_names = [country.name for country in longest_longitudes]

    longest_latitudes = total_country_list.order_by('-latitude')[:10]
    lat_values = [country.latitude for country in longest_latitudes]
    lat_names = [country.name for country in longest_latitudes]

    PROPERTIES.update({'position': 'Z2', 'x_title': 'Countries', 'y_title': 'longitudes', 'main_title': 'Greatest longitudes',
                    'graph_values': long_values, 'labels': long_names, 'figsize': (10, 4), 'marker': 'o', 'linestyle': '-'})

    line(ws, PROPERTIES)

    PROPERTIES.update({'position': 'Z28', 'x_title': 'Countries', 'y_title': 'latitudes', 'main_title': 'Greates latitudes',
                    'graph_values': lat_values, 'labels': lat_names, 'figsize': (10, 4)})

    line(ws, PROPERTIES)

    # Scatter graph

    area_list = [country.area for country in total_country_list]
    population_values = [country.population for country in total_country_list]

    PROPERTIES.update({'position': 'AM12', 'graph_values': population_values, 'graph_values_b': area_list,
                    'main_title': 'Population vs Area', 'x_title': 'Population', 'y_title': 'Area'})

    scatter(ws, PROPERTIES)

    # Prepare your response as a .xlsx file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_estadisticas.xlsx'

    wb.save(response)
    return response
