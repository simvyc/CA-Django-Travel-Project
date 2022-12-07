from django.urls import path
from . import views

urlpatterns = [
    path('', views.offers, name='offers'),
    path('<slug:category_slug>/', views.offers, name='offers_by_category'),
    path('<slug:category_slug>/<slug:slug>/', views.purchase_detail, name='purchase_detail'),
    
]
