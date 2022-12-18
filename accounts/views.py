from django.shortcuts import render, redirect
from .forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.views import _cart_id
from carts.models import Cart, CartItem

# Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            phone_number = form.cleaned_data['phone_number']
            # user object
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            
            user.phone_number = phone_number
            user.save()
            
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account'
            message = render_to_string('account_verification_by_email.html', {
                'user': user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_to_send = email
            send_email = EmailMessage(mail_subject, message, to=[email_to_send])
            send_email.send()
            messages.success(request, 'Registration successful. We have sent a verification email to you.')
            return redirect('/login/?command=verification&email='+email)
        
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    for item in cart_item: #assing user to cart item
                        item.user = user
                        item.save()
                        
            except:
                print('Except block')
                pass
            
            
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password is not correct, Try Again')
            return redirect('login')
        
    return render(request, 'login.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged Out')
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email) # __exact checks if email is exactly the same in teh db, case sensitive
            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_to_send = email
            send_email = EmailMessage(mail_subject, message, to=[email_to_send])
            send_email.send()
            
            messages.success(request, 'Email sent for password reset.')
            return redirect('login')
        else:
            messages.error(request, 'Sorry, Account does not Exist')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    # this code is to know, if this secure request
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link expired.')
        return redirect('login')
    
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password was reset.')
            return redirect('login')
            
        else:
            messages.error(request, 'Oooops, password does not match.')
            return redirect('reset_password')
    
    
    else:
        return render(request, 'reset_password.html')
    
        