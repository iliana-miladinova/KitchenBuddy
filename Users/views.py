import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.conf import settings
import requests


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
            return render(request, 'Users/registration.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'An acount with this username already exists')
            return render(request, 'Users/registration.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already used')
            return render(request, 'Users/registration.html')
        
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Your account was created successfuly! Please, login.')
        return redirect('login')
    
    return render(request, 'Users/registration.html')

def login_view(request):
    if request.user.is_authenticated:
        redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password')
            return render(request, 'Users/login.html')
        
    return render(request, 'Users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile(user=request.user)
    
    if request.method == 'POST':
        user_profile.age = request.POST['age']
        user_profile.gender = request.POST['gender']
        user_profile.weight = request.POST['weight']
        user_profile.height = request.POST['height']
        user_profile.activity = request.POST['activity']

        if (not user_profile.age or not user_profile.gender or not user_profile.weight or not 
            user_profile.height or not user_profile.activity):
            messages.error(request, 'Some fields are not filled')
            context = {'user_profile': user_profile}
            return render(request, 'Users/profile.html', context)
        
        
        user_profile.age = int(user_profile.age)
        user_profile.weight = float(user_profile.weight)
        user_profile.height = float(user_profile.height)

        #Mifflin-St Jeor Equation
        if user_profile.gender == 'Male':
            bmr = 10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age + 5
        else:
            bmr = 10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age - 161
            
        ACTIVITY_FACTOR = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'very': 1.725
        }

        multiplier = ACTIVITY_FACTOR.get(user_profile.activity, 1.2)
        user_profile.calories = round(bmr * multiplier)
        user_profile.save()

    
    context = {
        'user_profile': user_profile
    }
    return render(request, 'Users/profile.html', context)


