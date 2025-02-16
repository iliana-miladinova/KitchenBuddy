from django.shortcuts import render
from django.conf import settings
from .models import Substitute
from ingredients.models import Ingredient
import requests
# Create your views here.

def get_substitute_ingredients(request, ingredient_id, recipe_id):
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
        substitute_ingredients = []
        error = None

        db_substitute_ingredients = Substitute.objects.filter(ingredient=ingredient)

        if db_substitute_ingredients.exists():
            for sub in db_substitute_ingredients:
                substitute_ingredients.append({
                    'name': sub.substitute_ingredient.name,
                    'category': sub.substitute_ingredient.category
                })
        else:
            headers = {
                "X-RapidAPI-Key": settings.RAPID_API_KEY,
                "X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com"
            }

            ing_response = requests.get(
                "https://edamam-food-and-grocery-database.p.rapidapi.com/api/food-database/v2/parser",
                headers = headers,
                params = {'ingr':ingredient.name}
            )
        
            ing_data = ing_response.json()
            MY_KEY='hints'

            if MY_KEY in ing_data:
                for ing in ing_data[MY_KEY][:3]:
                    food = ing.get('food', {})
                    name = food.get('label')
                    food_category = food.get('category')

                    if name and name.lower() != ingredient.name.lower():
                        substitute_ingredients.append({
                            'name': name,
                            'category': food_category
                        })
                if not substitute_ingredients:
                    error = 'No substitude ingredients found'
            else:
                error = 'No substitude ingredients data found'
    except Exception as e:
        error = f"Error: {e}"

    context = {
        'ingredient': ingredient,
        'substitute_ingredients': substitute_ingredients,
        'error': error,
        'recipe_id': recipe_id
    }

    return render(request, 'substitutionIngredients/substitute_ingredients.html', context)