from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login ,logout
from .models import CustomUser  # Assuming you have a CustomUser model
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.cache import never_cache


from django.contrib.auth.decorators import login_required

# Create your views here.
@never_cache
def index(request):
    
    return render(request,'index.html')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']  # Make sure this matches your form field name
        user_type = request.POST['user_type']

        # Check if the email already exists in the database
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Email address is already in use.'})
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'username already used'})

        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        try:
            # Try to create a new user object
            user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
            # You may want to do additional processing here if needed
            return redirect('login')# Redirect to login page after successful registration
        except IntegrityError:
            # Handle the case where there is a database integrity error
            return render(request, 'register.html', {'error_message': 'An error occurred during registration.'})

    return render(request, 'register.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 'technician':
                request.session['user_type'] = 'technician'
                return redirect('technician_profile')  # Assuming you have a URL pattern named 'technician_profile'
            elif user.user_type == 'customer':
                request.session['user_type'] = 'customer'
                return redirect('customer_profile')  # Assuming you have a URL pattern named 'customer_profile'
            else:
                return HttpResponse('Invalid user type')  # Handle other user types if needed
        else:
            if not CustomUser.objects.filter(username=username).exists():
                error_message = 'Wrong username'
            else:
                error_message = 'Wrong password'

            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

@login_required(login_url='login')
@never_cache
def technician_profile(request):
    return render(request,'technician_profile.html')

@login_required(login_url='login')
@never_cache
def customer_profile(request):
    return render(request,'customer_profile.html')


def userLogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def services(request):
    return render(request,'services.html')



