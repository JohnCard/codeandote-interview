from django.db import models

# Create your models here.

class Country(models.Model):
    # Country name
    name = models.CharField(verbose_name='Nombre del País', max_length=20, unique=True, null=False, blank=False)
    # Country - region
    region = models.CharField(verbose_name='Región', max_length=20, null=False, blank=False)
    # Country - subregion
    subregion = models.CharField(verbose_name='Sub región', max_length=20, null=False, blank=False)
    # Country - capital
    capital = models.CharField(verbose_name='Capital', default='Unknown', max_length=20, null=True, blank=True)
    # Country - population
    population = models.IntegerField(verbose_name='Población total', null=False, blank=False)
    # Country - latitude
    latitude = models.IntegerField(verbose_name='Latitud', null=False, blank=False)
    # Country - longitude
    longitude  = models.IntegerField(verbose_name='Longitud', null=False, blank=False)
    # Country - area
    area = models.FloatField(verbose_name='Área', null=False, blank=False)
    # Country - flag
    flag = models.TextField(verbose_name='Bandera descriptiva', null=False, blank=True)