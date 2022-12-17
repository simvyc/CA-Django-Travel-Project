from django.contrib import admin
from offers.models import Purchase, ReviewAndRating

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('purchase_name', 'description', 'price', 'country', 'city', 'created_date', 'is_available', 'tickets')
    prepopulated_fields = {'slug': ('purchase_name',)}



admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ReviewAndRating)