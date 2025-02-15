from django.test import TestCase, Client
from django.urls import reverse
from ingredients.models import Ingredient
from recipe.models import Recipe, IngredientsDetails
from foodPreference.models import Diet, Allergy
from django.contrib.auth.models import User

class TestIngredientsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_recipes_by_ingredients')

        self.ingredient1 = Ingredient.objects.create(name='my_ingredient1', category='fruits')
        self.ingredient2 = Ingredient.objects.create(name='my_ingredient2', category='vegetables')

        self.diet = Diet.objects.create(name='my_diet')
        self.allergy = Allergy.objects.create(name='my_allergy')

        self.user = User.objects.create(username='iliana20', email='iliana@abv.bg', password='8888')
        self.recipe = Recipe.objects.create(user=self.user, title='my_recipe', description='my_description')

        IngredientsDetails.objects.create(recipe=self.recipe, ingredient=self.ingredient1, quantity=3, amount='grama')
        IngredientsDetails.objects.create(recipe=self.recipe, ingredient=self.ingredient2, quantity=8, amount='kg')
        self.recipe.ingredients.add(self.ingredient1, self.ingredient2)
        self.recipe.diet.add(self.diet)
        self.recipe.allergies.add(self.allergy)

        self.ingredient_not_in_recipe = Ingredient.objects.create(name='my_ingredient3', category='fruits')

    def test_ingredients_view_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ingredients/get_recipes_by_ingredients.html')
        self.assertIn('ingredients', response.context)
        self.assertIn('diets', response.context)
        self.assertIn('allergies', response.context)
        self.assertIn('recipes', response.context)

    def test_ingredients_view_post(self):
        data = {
            'ingredients': [self.ingredient1.id, self.ingredient2.id],
            'diet': self.diet.id,
            'allergy': self.allergy.id
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.recipe, response.context['recipes'])

    def test_ingredients_view_post_no_result(self):
        data = {
            'ingredients': [self.ingredient1.id, self.ingredient_not_in_recipe.id],
            'allergy': self.allergy.id
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.recipe, response.context['recipes'])