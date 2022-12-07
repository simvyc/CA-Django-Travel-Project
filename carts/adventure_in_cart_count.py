from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0 
    cart = Cart.objects.filter(cart_id=_cart_id(request)) #_cart_id contains the session key
    cart_items = CartItem.objects.all().filter(cart=cart[:1])
    for cart_item in cart_items:
        cart_count = cart_count + cart_item.persons
    return dict(cart_count=cart_count)