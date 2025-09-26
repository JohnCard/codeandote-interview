import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Contiene
    name_inits = django_filters.CharFilter(field_name='name', lookup_expr='istartswith')  # Inicia con
    name_ends = django_filters.CharFilter(field_name='name', lookup_expr='iendswith')  # Termina con
    price_range = django_filters.RangeFilter(field_name='price')
    price_maj = django_filters.NumberFilter(field_name='price', lookup_expr='gt')  # Mayor que
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['name', 'name_inits', 'name_ends', 'price_range', 'price_maj', 'price_min']
