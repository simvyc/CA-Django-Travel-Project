from django.db import models
from offers.models import Purchase, Variation
from accounts.models import Account

class Cart(models.Model):
    cart_id = models.CharField(max_length=200, blank=True)
    date_added =models.DateField(auto_now=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    persons = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.purchase.price * self.persons
    
    def __unicode__(self):
        return self.purchase
    