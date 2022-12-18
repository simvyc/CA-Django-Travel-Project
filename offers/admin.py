from django.contrib import admin
from offers.models import Purchase, ReviewAndRating, Variation

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('purchase_name', 'description', 'price', 'country', 'city', 'created_date', 'is_available', 'persons')
    prepopulated_fields = {'slug': ('purchase_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'variation', 'variation_value', 'created_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('purchase', 'variation', 'variation_value', 'created_date', 'is_active')
    

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ReviewAndRating)
admin.site.register(Variation, VariationAdmin)
