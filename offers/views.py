from django.shortcuts import render, get_object_or_404
from offers.models import Purchase
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def offers(request, category_slug=None):
    categories = None
    purchases = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        purchases = Purchase.objects.filter(category=categories, is_available=True)
        paginator = Paginator(purchases, 4)
        page = request.GET.get('page')
        paged_purchases = paginator.get_page(page)
        purchase_count = purchases.count()
    else:
            
        purchases = Purchase.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(purchases, 6)
        page = request.GET.get('page')
        paged_purchases = paginator.get_page(page)
        purchase_count = purchases.count()
        
        
    context = {
        'purchases': paged_purchases, 
        'purchase_count': purchase_count, 
    }
    return render(request, 'offers/offers.html', context)

def purchase_detail(request, category_slug, slug):
    try:
        single_purchase = Purchase.objects.get(category__slug=category_slug, slug=slug)
        is_in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), purchase=single_purchase).exists()

        
    except Exception as e:
        raise e
    
    context={
        'single_purchase': single_purchase,
        'is_in_cart': is_in_cart,
    }
    return render(request, 'offers/purchase_detail.html', context)