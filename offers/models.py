from django.db import models
from category.models import Category
from travelapp.models import Country, City
from accounts.models import Account
from django.urls import reverse

class Purchase(models.Model):
    purchase_name = models.CharField('Name', max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=2000, blank=True)
    price = models.IntegerField()
    image = models.ImageField('Image', upload_to='./travelapp/media/travels', blank=True) #null=True
    is_available = models.BooleanField(default=True)
    tickets = models.IntegerField(default=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Select category') # when delete category, travels with that cat will be deleted
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, help_text='Select country')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, help_text='Select city')
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('purchase_detail', args=[self.category.slug, self.slug])
        

    def __str__(self):
        return self.purchase_name
    
class ReviewAndRating(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=120, blank=True)
    review = models.TextField(max_length=1000, blank=True)
    rating = models.IntegerField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject