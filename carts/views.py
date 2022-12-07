from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from offers.models import Purchase
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id) # get the puchase
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(purchase=purchase, cart=cart)
        cart_item.persons += 1 #add more persons to the travel
        cart_item.save()
    
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            purchase = purchase,
            persons = 1,
            cart = cart,
        )
        cart_item.save()
    
    return redirect('cart')
    
def remove_cart(request, purchase_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    purchase = get_object_or_404(Purchase, id=purchase_id)
    cart_item = CartItem.objects.get(purchase=purchase, cart=cart)
    if cart_item.persons > 1:
        cart_item.persons -= 1 
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, purchase_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    purchase = get_object_or_404(Purchase, id=purchase_id)
    cart_item = CartItem.objects.get(purchase=purchase, cart=cart)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, persons=0, cart_items=None):
    tax=0
    t_total=0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # take cart obj by id
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.purchase.price * cart_item.persons)
            persons += cart_item.persons
        tax = (21 * total)/100
        t_total = total + tax
            
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'persons': persons,
        'cart_items': cart_items,
        'tax': tax,
        't_total': t_total,
    }
    
    return render(request, 'offers/cart.html', context)