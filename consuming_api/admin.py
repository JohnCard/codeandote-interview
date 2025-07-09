from django.contrib import admin
from .models import Country

# Register your models here.

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'subregion', 'capital', 'population')
    search_fields = ('id', 'name', 'region', 'subregion')
    list_filter = ('name', 'region')
    ordering = ['id', 'name', 'region', 'subregion']

admin.site.register(Country, CountryAdmin)