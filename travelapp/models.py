from django.db import models
# from django.urls import reverse
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    country_name = models.CharField('Country', max_length=30, help_text='Select or create country')
        
    def __str__(self):
        return self.country_name
        
    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'
            
class City(models.Model):
    city_name = models.CharField('City',  max_length=200, help_text='Select the city')
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
                
    def __str__(self):
        return self.city_name
    
    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        
        
