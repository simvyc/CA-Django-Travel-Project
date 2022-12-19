from django.shortcuts import render, get_object_or_404, redirect
from offers.models import Purchase, ReviewAndRating
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm
from django.contrib import messages
from django.http import HttpResponseRedirect


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
        paginator = Paginator(purchases, 4)
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
    
        
    reviews = ReviewAndRating.objects.filter(purchase_id=single_purchase.id, status=True)

    context={
        'single_purchase': single_purchase,
        'is_in_cart': is_in_cart,
        'reviews': reviews,
    }
    return render(request, 'offers/purchase_detail.html', context)
        
def post_review(request, purchase_id):

    if request.method == 'POST':
        try:
            reviews = ReviewAndRating.objects.get(user__id=request.user.id, purchase__id=purchase_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except ReviewAndRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewAndRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.purchase_id = purchase_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
