from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField('Name', max_length=200, help_text='Select or create category', unique=True)
    slug = models.SlugField(max_length = 100, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        return reverse('offers_by_category', args=[self.slug])


    def __str__(self):
        return self.category_name