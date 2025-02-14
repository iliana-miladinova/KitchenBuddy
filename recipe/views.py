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
        'allergies': allergies
    }

    return render(request, 'recipe/list_recipe.html', context)

@login_required
def recipe_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        #ingredients = request.POST['ingredients']
        cooking_time = request.POST['cooking_time']
        calories = request.POST['calories']
        dish_type = request.POST['dish_type']
        image = request.FILES['image']

        recipe = Recipe.objects.create(user=request.user, title=title, description=description,
                                       cooking_time=cooking_time, calories=calories, dish_type=dish_type,
                                       image=image)
        
        diets = request.POST.getlist('diet[]')
        if diets:
            recipe.diet.set(diets)
        
        allergies = request.POST.getlist('allergy[]')
        if allergies:
            recipe.allergies.set(allergies)

        ingredients = request.POST.getlist('ingredient[]')
        quantity = request.POST.getlist('quantity[]')
        amount = request.POST.getlist('amount[]')

        for ing in range(len(ingredients)):
            ingredient = Ingredient.objects.get(id=ingredients[ing])

            IngredientsDetails.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity[ing], amount=amount[ing])

        # context = {
        # 'ingredients': Ingredient.objects.all().order_by('category', 'name'),
        # 'dietary_preferences': Diet.objects.all().order_by('name'),  
        # 'allergens': Allergy.objects.all().order_by('name'),
        # 'users_recipes': Recipe.objects.filter(user=request.user),
        # 'all_recipes': Recipe.objects.all()
        # }
        
        return redirect('list_recipe')
    else:
        ingredients = Ingredient.objects.all().order_by('category', 'name')
        diets = Diet.objects.all().order_by('name')
        allergies = Allergy.objects.all().order_by('name')
        context = {
            'ingredients': ingredients,
            'diets': diets,
            'allergies': allergies
        }
        return render(request, 'recipe/create_recipe.html', context)

    
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
    #ingredients = recipe.ingredients.all()
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

def recipe_update(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.user:
        if request.method == 'POST':
            dish_type = request.POST.get('dish_type')
            if not dish_type:
                dish_type = recipe.dish_type 
        
            title = request.POST.get('title')
            description = request.POST.get('description')
            cooking_time = request.POST.get('cooking_time')
            calories = request.POST.get('calories')
            dish_type = request.POST.get('dish_type')
            
            recipe.title = title
            recipe.description = description
            recipe.cooking_time = cooking_time
            recipe.calories = calories
            recipe.dish_type = dish_type
        
            
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']

            recipe.save()

            #recipe.ingredients.all().delete()
            print("POST data:", request.POST)
            print("Files:", request.FILES)
            

            ingredients = request.POST.getlist('ingredient[]')
            quantity = request.POST.getlist('quantity[]')
            amount = request.POST.getlist('amount[]')

            print("Ingredients before processing:", ingredients)
            print("Quantities before processing:", quantity)
            print("Amounts before processing:", amount)
            #IngredientsDetails.objects.filter(recipe=recipe).delete()


            # if ingredients and quantity and amount and len(ingredients) == len(quantity) == len(amount):
            #     IngredientsDetails.objects.filter(recipe=recipe).delete()
            #     for ing in range(len(ingredients)):
            #         ingredient = Ingredient.objects.get(id=ingredients[ing])
            #         IngredientsDetails.objects.create(recipe=recipe, 
            #                                         ingredient=ingredient, 
            #                                         quantity=quantity[ing], 
            #                                         amount=amount[ing])

            try:
                # Изтрий старите съставки
                if ingredients and quantity and amount and len(ingredients) == len(quantity) == len(amount):
                    IngredientsDetails.objects.filter(recipe=recipe).delete()
                    for ing in range(len(ingredients)):
                        ingredient = Ingredient.objects.get(id=ingredients[ing])
                        IngredientsDetails.objects.create(recipe=recipe, 
                                                    ingredient=ingredient, 
                                                    quantity=quantity[ing], 
                                                    amount=amount[ing])
                        print(f"Ingredient {ingredient.name} created successfully")
                
                print("All ingredients processed")
                
            except Exception as e:
                print(f"Error processing ingredients: {e}")
           
            # for ing in range(len(ingredients)):
            #     ingredient = Ingredient.objects.get(id=ingredients[ing])

            #     IngredientsDetails.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity[ing], amount=amount[ing])
            
            # diets = request.POST.getlist('diet[]')
            # recipe.diet.clear()
            # for diet_id in diets:
            #     recipe.diet.add(diet_id)
            diets = request.POST.getlist('diet_name')
            if diets:
                recipe.diet.set(diets)

            # allergies = request.POST.getlist('allergy[]')
            # recipe.allergies.clear()
            # for allergy_id in allergies:
            #     recipe.allergies.add(allergy_id)

            allergies = request.POST.getlist('allergy[]')
            if allergies:
                recipe.allergies.set(allergies)

            
            return redirect('recipe_details', recipe_id=recipe_id)
        
    context = {
        'recipe': recipe,
        'ingredient': Ingredient.objects.all().order_by('category', 'name'),
        'diets': Diet.objects.all().order_by('name'),
        'allergies': Allergy.objects.all().order_by('name'),
        'current_ingredients': IngredientsDetails.objects.filter(recipe=recipe)
    }
    return render(request, 'recipe/recipe_update.html', context)



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

@login_required
def get_menu(request):
    try:
        user_profile = request.user.profile
        calories_per_day = user_profile.calories
    except Profile.DoesNotExist:
        calories_per_day = 2000
    
    calories_breakfast = calories_per_day * 0.25
    calories_lunch = calories_per_day * 0.4
    calories_dinner = calories_per_day * 0.35

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
    
    #breakfast_recipes = favourite_recipes.filter(dish_type='breakfast')
    breakfast_recipes = list(favourite_recipes.filter(dish_type='breakfast'))
    random.shuffle(breakfast_recipes)
    for recipe in breakfast_recipes:
        if recipe.calories <= calories_breakfast:
            menu['breakfast'] = recipe
            break

    #calories_lunch_remaining = calories_lunch
    starter_calories_lunch = calories_per_day * 0.1
    main_calories_lunch = calories_per_day * 0.25
    dessert_calories_lunch = calories_per_day * 0.05

    #starter_recipes = favourite_recipes.filter(dish_type='starter')
    starter_recipes = list(favourite_recipes.filter(dish_type='starter'))
    random.shuffle(starter_recipes)
    for recipe in starter_recipes:
        #starter_calories = calories_lunch_remaining * 0.1
        if recipe.calories <= starter_calories_lunch:
            menu['lunch']['starter'] = recipe
            #calories_lunch_remaining -= recipe.calories
            break

    #main_recipes = favourite_recipes.filter(dish_type='main')
    main_recipes = list(favourite_recipes.filter(dish_type='main'))
    random.shuffle(main_recipes)
    for recipe in main_recipes:
        if recipe.calories <= main_calories_lunch:
            menu['lunch']['main'] = recipe
            break

    #dessert_recipes = favourite_recipes.filter(dish_type='dessert')
    dessert_recipes = list(favourite_recipes.filter(dish_type='dessert'))
    random.shuffle(dessert_recipes)
    for recipe in dessert_recipes:
        if recipe.calories <= dessert_calories_lunch:
            menu['lunch']['dessert'] = recipe
            break

    starter_calories_dinner = calories_per_day * 0.1
    main_calories_dinner = calories_per_day * 0.20
    dessert_calories_dinner = calories_per_day * 0.05

    #starter_recipes = favourite_recipes.filter(dish_type='starter')
    starter_recipes = list(favourite_recipes.filter(dish_type='starter'))
    random.shuffle(starter_recipes)
    for recipe in starter_recipes:
        #starter_calories = calories_lunch_remaining * 0.1
        if recipe.calories <= starter_calories_dinner:
            menu['dinner']['starter'] = recipe
            #calories_lunch_remaining -= recipe.calories
            break

    #main_recipes = favourite_recipes.filter(dish_type='main')
    main_recipes = list(favourite_recipes.filter(dish_type='main'))
    random.shuffle(main_recipes)
    for recipe in main_recipes:
        if recipe.calories <= main_calories_dinner:
            menu['dinner']['main'] = recipe
            break

    #image.pngdessert_recipes = favourite_recipes.filter(dish_type='dessert')
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
