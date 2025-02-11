from django.shortcuts import render
from recipe.models import Recipe
from .models import Ingredient
from foodPreference.models import Diet, Allergy

def get_recipes_by_ingredients(request):
    ingredients = Ingredient.objects.all().order_by('category', 'name')
    diets = Diet.objects.all().order_by('name')
    allergies = Allergy.objects.all().order_by('name')

    suggested_recipes = []

    if request.method == 'POST':
        chosen_ingredients = request.POST.getlist('ingredients')
        chosen_diets = request.POST.getlist('diets')
        chosen_allergies = request.POST.getlist('allergies')

        if chosen_ingredients:
            chosen_ingredients = Ingredient.objects.filter(id__in=chosen_ingredients)

            suggested_recipes = Recipe.objects.all()
            for ing in chosen_ingredients:
                suggested_recipes = suggested_recipes.filter(ingredients=ing)
            
            if chosen_diets:
                suggested_recipes=suggested_recipes.filter(diet__id__in=chosen_diets).distinct()

            if chosen_allergies:
                suggested_recipes=suggested_recipes.exclude(allergies__id__in=chosen_allergies).distinct()

    context = {'ingredients': ingredients, 
               'recipes': suggested_recipes, 
               'diets': diets,
               'allergies': allergies}

    return render(request, 'ingredients/get_recipes_by_ingredients.html', context)
