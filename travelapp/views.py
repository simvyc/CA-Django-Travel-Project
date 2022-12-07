from django.shortcuts import render
from offers.models import Purchase
# from django.http import HttpResponse

# Create your views here.

def home(request):
    purchases = Purchase.objects.all().filter(is_available=True)
    context = {
        'purchases': purchases, 
    }
    
    return render(request, 'home.html', context)

def about(request):
    text = "Some text"
    context = {
        'text': text, 
    }
    
    return render(request, 'about.html', context)