from django.db import models
from category.models import Category
from travelapp.models import Country, City
from accounts.models import Account
from django.urls import reverse
from django.db.models import Avg, Count

class Purchase(models.Model):
    purchase_name = models.CharField('Name', max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=2000, blank=True)
    price = models.IntegerField()
    image = models.ImageField('Image', upload_to='./travelapp/media/travels', blank=True) #null=True
    is_available = models.BooleanField(default=True)
    persons = models.IntegerField(default=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Select category') # when delete category, travels with that cat will be deleted
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, help_text='Select country')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, help_text='Select city')
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('purchase_detail', args=[self.category.slug, self.slug])
    
    def averageReview(self):
        reviews = ReviewAndRating.objects.filter(purchase=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewAndRating.objects.filter(purchase=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def __str__(self):
        return self.purchase_name

class VariationManager(models.Manager):
    def datetimes(self):
        return super(VariationManager, self).filter(variation='datetime', is_active=True)
    
variation_choice = (
    ('datetime', 'datetime'),
)

class Variation(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    variation = models.CharField(max_length=100, choices=variation_choice)
    variation_value = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    
    
    objects = VariationManager()
    
    def __unicode__(self):
        return self.variation_value
    
   
class ReviewAndRating(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=120, blank=True)
    review = models.TextField(max_length=1000, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject