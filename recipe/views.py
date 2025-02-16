from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from .models import Recipe, Rating, Comment, IngredientsDetails
from ingredients.models import Ingredient
from foodPreference.models import Allergy, Diet
from Users.models import Profile
import random
from django.forms import inlineformset_factory
from .forms import IngredientsDetailsForm

# Create your views here.
@login_required
def list_recipe(request):
    sort_by = request.GET.get('sort_by', 'title') 

    sorting_options = {'title': 'title',
                       'rating': '-average_rating',
                       'cooking_time': 'cooking_time',
                       'calories': 'calories'}

    sorting = sorting_options.get(sort_by, 'title')

    #Get all the recipes per user
    users_recipes = Recipe.objects.filter(user=request.user).order_by(sorting)

    #Get all the recipes
    all_recipes = Recipe.objects.all().order_by(sorting)
    ingredients = Ingredient.objects.all().order_by('category', 'name')

    diets = Diet.objects.all().order_by('name')
    allergies = Allergy.objects.all().order_by('name')

    filtered_recipes_diets = request.GET.getlist('diets_filter')
    if filtered_recipes_diets:
        users_recipes = users_recipes.filter(diet__id__in=filtered_recipes_diets).distinct()
        all_recipes = all_recipes.filter(diet__id__in=filtered_recipes_diets).distinct()

    filtered_recipes_allergies = request.GET.getlist('allergies_filter')
    if filtered_recipes_allergies:
        users_recipes = users_recipes.exclude(allergies__id__in=filtered_recipes_allergies).distinct()
        all_recipes=all_recipes.exclude(allergies__id__in=filtered_recipes_allergies).distinct()

    context = {
        'users_recipes': users_recipes,
        'all_recipes': all_recipes,
        'sort_by': sort_by,
        'sorting_options': sorting_options,
        'ingredients': ingredients,
        'diets': diets,          
        'allergies': allergies,
        'diets_filter': filtered_recipes_diets,
        'allergies_filter': filtered_recipes_allergies
    }

    return render(request, 'recipe/list_recipe.html', context)

@login_required
def recipe_create(request):
    IngredientsForm = inlineformset_factory(
        Recipe, 
        IngredientsDetails, 
        form=IngredientsDetailsForm,
        extra=20, # Broyat na praznite formi
        can_delete=True
    )

    if request.method == 'POST':
        ingredients_form = IngredientsForm(request.POST, request.FILES)
        if ingredients_form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            cooking_time = request.POST['cooking_time']
            calories = request.POST['calories']
            dish_type = request.POST['dish_type']
            image = request.FILES['image']

            recipe = Recipe.objects.create(user=request.user, title=title, description=description,
                                       cooking_time=cooking_time, calories=calories, dish_type=dish_type,
                                       image=image)
            
            ingredients_form.instance = recipe
            ingredients_form.save()
        
            diets = request.POST.getlist('diet_list')
            if diets:
                recipe.diet.set(diets)
        
            allergies = request.POST.getlist('allergy_list')
            if allergies:
                recipe.allergies.set(allergies)

        return redirect('list_recipe')
    
    else:
        ingredients_form = IngredientsForm()
        ingredients = Ingredient.objects.all().order_by('category', 'name')
        diets = Diet.objects.all().order_by('name')
        allergies = Allergy.objects.all().order_by('name')

        context = {
            'ingredients': ingredients,
            'diets': diets,
            'allergies': allergies,
            'ingredients_form': ingredients_form
        }

        return render(request, 'recipe/create_recipe.html', context)

@login_required
def recipe_delete(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if recipe.user != request.user:
            return redirect('recipe_details', recipe_id=recipe_id)
        
        recipe.delete()
        return redirect('list_recipe')
    
    return redirect('list_recipe')
    
@login_required
def add_remove_favourite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user not in recipe.favourite.all():
        recipe.favourite.add(request.user)
    else:
        recipe.favourite.remove(request.user)
    
    return redirect('recipe_details', recipe_id=recipe_id)

@login_required
def favourite_recipes(request):
    favourite_recipes = Recipe.objects.filter(favourite=request.user)

    context = {
        'favourite_recipes': favourite_recipes
    }

    return render(request, 'recipe/favourite_recipes.html', context)

@login_required
def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = IngredientsDetails.objects.filter(recipe=recipe)
    comments = recipe.comment.all()
    is_favourite_recipe = recipe.favourite.filter(id=request.user.id).exists()


    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'comments': comments,
        'is_favourite_recipe': is_favourite_recipe
    }

    return render(request, 'recipe/recipe_details.html', context)

@login_required
def recipe_update(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.user:
        IngredientsForm = inlineformset_factory(Recipe, IngredientsDetails,
                                                 form=IngredientsDetailsForm, extra=20,
                                                 can_delete=True)
        
        error_message = None
        if request.method == 'POST':
            try:
                dish_type = request.POST.get('dish_type')
                if not dish_type:
                    dish_type = recipe.dish_type 
        
                title = request.POST.get('title')
                description = request.POST.get('description')
                cooking_time = request.POST.get('cooking_time')
                calories = request.POST.get('calories')
                dish_type = request.POST.get('dish_type')

                ingredients_form = IngredientsForm(request.POST, instance=recipe)
                if not ingredients_form.is_valid():
                    error_message = 'Invalid ingredients.'
                    raise ValueError(error_message)
            
                recipe.title = title
                recipe.description = description
                recipe.cooking_time = cooking_time
                recipe.calories = calories
                recipe.dish_type = dish_type
        
                if 'image' in request.FILES:
                    recipe.image = request.FILES['image']

                recipe.save()
                ingredients_form.save()

                diets = request.POST.getlist('diet_list')
                if diets:
                    recipe.diet.set(diets)

                allergies = request.POST.getlist('allergy_list')
                if allergies:
                    recipe.allergies.set(allergies)

            
                return redirect('recipe_details', recipe_id=recipe_id)
            except Exception as e:
                error_message = f'Error: {str(e)}'
        else:
            ingredients_form = IngredientsForm(instance=recipe)
    
    ingredient = Ingredient.objects.all().order_by('category', 'name')
    diet = Diet.objects.all().order_by('name')
    allergy = Allergy.objects.all().order_by('name')
    current_ingredients = IngredientsDetails.objects.filter(recipe=recipe)

    context = {
        'recipe': recipe,
        'ingredient': ingredient,
        'diets': diet,
        'allergies': allergy,
        'current_ingredients': current_ingredients,
        'ingredients_form': ingredients_form,
        'error_message': error_message
    }

    return render(request, 'recipe/recipe_update.html', context)

@login_required
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
    
    return redirect('recipe_details', recipe_id=recipe_id)

@login_required
def add_comment(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)

        comment_text = request.POST['comment']

        if comment_text:
            Comment.objects.create(recipe=recipe, user=request.user, comment=comment_text)
        
        return redirect('recipe_details', recipe_id=recipe_id)
    
    return redirect('recipe_details', recipe_id=recipe_id)

@login_required
def get_menu(request):
    try:
        user_profile = request.user.profile
        calories_per_day = user_profile.calories
    except Profile.DoesNotExist:
        calories_per_day = 2000
    
    calories_breakfast = calories_per_day * 0.25
    #calories_lunch ------ calories_per_day * 0.4
    #calories_dinner ------ calories_per_day * 0.35

    favourite_recipes = Recipe.objects.filter(favourite=request.user)

    menu = {
        'breakfast': None,
        'lunch': {
            'starter': None,
            'main': None,
            'dessert': None
        },
        'dinner': {
            'starter': None,
            'main': None,
            'dessert': None
        }
    }
    
    breakfast_recipes = list(favourite_recipes.filter(dish_type='breakfast'))
    random.shuffle(breakfast_recipes)
    for recipe in breakfast_recipes:
        if recipe.calories <= calories_breakfast:
            menu['breakfast'] = recipe
            break

    starter_calories_lunch = calories_per_day * 0.1
    main_calories_lunch = calories_per_day * 0.25
    dessert_calories_lunch = calories_per_day * 0.05

    starter_recipes = list(favourite_recipes.filter(dish_type='starter'))
    random.shuffle(starter_recipes)
    for recipe in starter_recipes:
        if recipe.calories <= starter_calories_lunch:
            menu['lunch']['starter'] = recipe
            break

    main_recipes = list(favourite_recipes.filter(dish_type='main'))
    random.shuffle(main_recipes)
    for recipe in main_recipes:
        if recipe.calories <= main_calories_lunch:
            menu['lunch']['main'] = recipe
            break

    dessert_recipes = list(favourite_recipes.filter(dish_type='dessert'))
    random.shuffle(dessert_recipes)
    for recipe in dessert_recipes:
        if recipe.calories <= dessert_calories_lunch:
            menu['lunch']['dessert'] = recipe
            break

    starter_calories_dinner = calories_per_day * 0.1
    main_calories_dinner = calories_per_day * 0.20
    dessert_calories_dinner = calories_per_day * 0.05

    starter_recipes = list(favourite_recipes.filter(dish_type='starter'))
    random.shuffle(starter_recipes)
    for recipe in starter_recipes:
        if recipe.calories <= starter_calories_dinner:
            menu['dinner']['starter'] = recipe
            break

    main_recipes = list(favourite_recipes.filter(dish_type='main'))
    random.shuffle(main_recipes)
    for recipe in main_recipes:
        if recipe.calories <= main_calories_dinner:
            menu['dinner']['main'] = recipe
            break

    dessert_recipes = list(favourite_recipes.filter(dish_type='dessert'))
    random.shuffle(dessert_recipes)
    for recipe in dessert_recipes:
        if recipe.calories <= dessert_calories_dinner:
            menu['dinner']['dessert'] = recipe
            break

    total_calories_menu = 0
    if menu['breakfast']:
        total_calories_menu += menu['breakfast'].calories

    for course in ['starter', 'main', 'dessert']:
        if menu['lunch'][course]:
            total_calories_menu += menu['lunch'][course].calories
        if menu['dinner'][course]:
            total_calories_menu += menu['dinner'][course].calories

    context = {
        'menu': menu,
        'total_calories_menu': total_calories_menu,
        'recommended_calories': calories_per_day
    }

    return render(request, 'recipe/get_menu.html', context)