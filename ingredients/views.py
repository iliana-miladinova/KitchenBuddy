from django.shortcuts import render
from recipe.models import Recipe
from .models import Ingredient

def get_recipes_by_ingredients(request):
    ingredients = Ingredient.objects.all().order_by('category', 'name')

    suggested_recipes = []

    if request.method == 'POST':
        chosen_ingredients = request.POST.getlist('ingredients')
        if chosen_ingredients:
            chosen_ingredients = Ingredient.objects.filter(id__in=chosen_ingredients)

            suggested_recipes = Recipe.objects.all()
            for ing in chosen_ingredients:
                suggested_recipes = suggested_recipes.filter(ingredients=ing)

    context = {'ingredients': ingredients, 'recipes': suggested_recipes }

    return render(request, 'ingredients/get_recipes_by_ingredients.html', context)
