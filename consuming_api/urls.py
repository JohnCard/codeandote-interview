from django.urls import path
from .views import CountryAPIView, CountryRetrieveUpdateDestroyAPIView, CreateCountry, excel_report

urlpatterns = [
    # Create & list country instances
    path('countries', CountryAPIView.as_view(), name='countries'),
    # Retrieve, update & delete country instances
    path('countries/<int:id>', CountryRetrieveUpdateDestroyAPIView.as_view(), name='country'),
    # Create one specific country by it´s name & update masive data for Country model
    path('generic', CreateCountry.as_view(), name='generic'),
    # Create an excel summary about your main data
    path('excel_report', excel_report, name='excel-report')
]