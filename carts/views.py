from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from offers.models import Purchase, Variation
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, purchase_id):
    current_user = request.user
    purchase = Purchase.objects.get(id=purchase_id) #get the purchase
    # If the user is authenticated
    if current_user.is_authenticated:
        purchase_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(purchase=purchase, variation__iexact=key, variation_value__iexact=value)
                    purchase_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(purchase=purchase, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(purchase=purchase, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if purchase_variation in ex_var_list:
                # increase ticket(persons) quantity
                index = ex_var_list.index(purchase_variation)
                item_id = id[index]
                item = CartItem.objects.get(purchase=purchase, id=item_id)
                item.persons += 1
                item.save()

            else:
                item = CartItem.objects.create(purchase=purchase, persons=1, user=current_user)
                if len(purchase_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*purchase_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                purchase = purchase,
                persons = 1,
                user = current_user,
            )
            if len(purchase_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*purchase_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        purchase_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(purchase=purchase, variation__iexact=key, variation_value__iexact=value)
                    purchase_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(purchase=purchase, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(purchase=purchase, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if purchase_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(purchase_variation)
                item_id = id[index]
                item = CartItem.objects.get(purchase=purchase, id=item_id)
                item.persons += 1
                item.save()

            else:
                item = CartItem.objects.create(purchase=purchase, persons=1, cart=cart)
                if len(purchase_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*purchase_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                purchase = purchase,
                persons = 1,
                cart = cart,
            )
            if len(purchase_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*purchase_variation)
            cart_item.save()
        return redirect('cart')   

def remove_cart(request, purchase_id, cart_item_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(purchase=purchase, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # !
            cart_item = CartItem.objects.get(purchase=purchase, cart=cart, id=cart_item_id)
        if cart_item.persons > 1:
            cart_item.persons -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, purchase_id, cart_item_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(purchase=purchase, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(purchase=purchase, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, persons=0, cart_items=None):
    try:
        tax=0
        t_total=0
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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





@login_required(login_url='login')
def checkout(request, total=0, persons=0, cart_items=None):

    try:
        tax=0
        t_total=0
        if request.user.is_authenticated:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # take cart obj by id
        else:
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
    return render(request, 'offers/checkout.html', context)


def order_checkout(request):
    return render(request, 'offers/order_checkout.html')

