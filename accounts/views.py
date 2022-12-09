from django.shortcuts import render, redirect
from .forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

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
            messages.success(request, 'Registration successful')
            return redirect('register')
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
            auth.login(request, user)
            # messages.success(request, 'Welcome, you are loogged in! :) ')
            return redirect('home')
        else:
            messages.error(request, 'Email or password is not correct, Try Again')
            return redirect('login')
        
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged Out')
    return redirect('login')