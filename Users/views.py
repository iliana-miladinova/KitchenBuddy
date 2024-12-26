import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(EMAIL_REGEX, email):
            messages.error(request, 'Invalid email format')
            return render(request, 'Users/registration.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'User/registration.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'An acount with this username already exists')
            return render(request, 'User/registration.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already used')
            return render(request, 'User/registration.html')
        
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Your account was created successfuly! Please, login.')
        return redirect('login')
    
    return render(request, 'User/registration.html')

def login_view(request):
    if request.user.is_authenticated:
        redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            redirect('home')
        else:
            messages.error(request, 'Incorrect username or password')
            return render(request, 'User/login.html')
        
    return render(request, 'Users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

    