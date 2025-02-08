from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from .models import Recipe, Rating, Comment

# Create your views here.
@login_required
def list_recipe(request):
    sort_by = request.GET.get('sort_by', 'title') 
    sorting_options = {'title': 'title',
                       'rating': 'average_rating',
                       'cooking_time': 'cooking_time',
                       'calories': 'calories'}

    sorting = sorting_options.get(sort_by, 'title')
    #Get all the recipes per user
    #users_recipes = Recipe.objects.filter(user=request.user).order_by(sorting)

    #Get all the recipes
    all_recipes = Recipe.objects.all().order_by(sorting)

    context = {
        #'users_recipes': users_recipes,
        'all_recipes': all_recipes,
        'sort_by': sort_by,
        'sorting_options': sorting_options
    }

    return render(request, 'recipe/list_recipe.html', context)

@login_required
def recipe_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        cooking_time = request.POST['cooking_time']
        calories = request.POST['calories']
        image = request.FILES['image']

        recipe = Recipe.objects.create(user=request.user, title=title, description=description,
                                       ingredients=ingredients, cooking_time=cooking_time, calories=calories,
                                       image=image)
        
        return redirect('list_recipe')

@login_required
def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comment.all()

    context = {
        'recipe': recipe,
        'comments': comments
    }

    return render(request, 'recipe/recipe_details.html', context)

def recipe_update(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.user:
        if request.method == 'POST':
        # Get form data
            title = request.POST['title']
            description = request.POST['description']
            ingredients = request.POST['ingredients']
            cooking_time = request.POST['cooking_time']
            calories = request.POST['calories']
        
        # Update recipe fields
            recipe.title = title
            recipe.description = description
            recipe.ingredients = ingredients
            recipe.cooking_time = cooking_time
            recipe.calories = calories
        
            # Handle image update if provided
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']

            recipe.save()
            return redirect('recipe_details', recipe_id=recipe_id)
        
    return redirect('recipe_details', recipe_id=recipe_id)



def add_rating(request, recipe_id):
    if request.method =='POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        rating_val = request.POST['rating']

        try:
            rating = Rating.objects.get(recipe=recipe, user=request.user)
            rating.rating_val = rating_val
            rating.save()
        except Rating.DoesNotExist:
            Rating.objects.create(recipe=recipe, user=request.user, rating_val=rating_val)

        return redirect('recipe_details', recipe_id=recipe_id)
    
    #??????
    return redirect('recipe_details', recipe_id=recipe_id)

def add_comment(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)

        comment_text = request.POST['comment']

        if comment_text:
            Comment.objects.create(recipe=recipe, user=request.user, comment=comment_text)
        
        return redirect('recipe_details', recipe_id=recipe_id)
    
    #??????
    return redirect('recipe_details', recipe_id=recipe_id)
