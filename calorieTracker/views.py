from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CalorieTracker
from recipe.models import Recipe
from Users.models import Profile

# Create your views here.
@login_required
def list_calorie_tracker(request):
    try:
        user_profile = request.user.profile
        calorie_limit = user_profile.calories
    except Profile.DoesNotExist:
        user_profile = None
        calorie_limit = 2000

    recipes_in_tracker = CalorieTracker.objects.filter(user=request.user)
    calories_sum = CalorieTracker.get_total_calories(request.user)

    remaining_calories = calorie_limit - calories_sum
    no_left_calories = remaining_calories <= 0
    if no_left_calories:
        messages.warning(request, "You have eaten enough :)")


    context = {
        'recipes_in_tracker': recipes_in_tracker,
        'calories_sum': calories_sum,
        'remaining_calories': remaining_calories,
        'calorie_limit': calorie_limit,
        'no_left_calories': no_left_calories,
        'user_profile': user_profile

    }

    return render(request, 'calorieTracker/list_calorie_tracker.html', context)

@login_required
def add_to_calorie_tracker(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if CalorieTracker.objects.filter(user=request.user, recipe=recipe).exists():
        return redirect('recipe_details', recipe_id=recipe_id)
    
    CalorieTracker.objects.create(user=request.user, recipe=recipe)

    return redirect('list_calorie_tracker')

@login_required
def remove_from_calorie_tracker(request, recipe_id):
    recipe_in_tracker = get_object_or_404(CalorieTracker, user=request.user, recipe_id=recipe_id)
    recipe_in_tracker.delete()
    return redirect('list_calorie_tracker')

@login_required
def edit_servings(request, recipe_id):
    recipe_in_tracker = get_object_or_404(CalorieTracker, user=request.user, recipe_id=recipe_id)
    
    if request.method == 'POST':
        new_servings = int(request.POST['servings'])
        recipe_in_tracker.servings = new_servings
        recipe_in_tracker.save()

        return redirect('list_calorie_tracker')
    
    context = {
        'recipe_in_tracker': recipe_in_tracker
    }

    return render(request, 'calorieTracker/edit_servings.html', context)
        
    
    


