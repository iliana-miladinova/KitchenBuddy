from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from ingredients.models import Ingredient
from recipe.models import Recipe
from substitutionIngredients.models import Substitute


class TestSubstituteIngredientsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')

        self.recipe = Recipe.objects.create(
            user = self.user,
            title = 'my_recipe',
            description = 'my_description',
            cooking_time = 30,
            dish_type = 'main'
        )

        self.ingredient = Ingredient.objects.create(name = 'Daisy', category = 'vegetables')

        self.url = reverse('show_substitutes', args=[self.ingredient.id, self.recipe.id])

    def test_get_substitute_ingredients_from_db(self):
        substitute = Ingredient.objects.create(name = 'Violet', category = 'vegetables')

        Substitute.objects.create(ingredient = self.ingredient, substitute_ingredient = substitute)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitutionIngredients/substitute_ingredients.html')

        substitutes = response.context['substitute_ingredients']

        self.assertEqual(len(substitutes), 1)
        self.assertEqual('Violet', substitutes[0]['name'])
        self.assertEqual('vegetables', substitutes[0]['category'])

    @patch('substitutionIngredients.views.requests.get')
    def test_get_substitute_ingredients_from_api(self, mock_get):
        mock_response = {
            'hints': [
                {
                    'food': {'label': 'Violet', 'category': 'vegetables'}
                },
                {
                    'food': {'label': 'Roses', 'category': 'vegetables'}
                },
                {
                    'food': {'label': 'Lily', 'category': 'vegetables'}
                },
                {
                    'food': {'label': 'Tulip', 'category': 'vegetables'}
                }
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get(self.url)
        substitutes = response.context['substitute_ingredients']
        self.assertEqual(len(substitutes), 3)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Violet', response.context['substitute_ingredients'][0]['name'])
        self.assertIn('Roses', response.context['substitute_ingredients'][1]['name'])
        self.assertIn('Lily', response.context['substitute_ingredients'][2]['name'])

    @patch('substitutionIngredients.views.requests.get')
    def test_no_substitute_ingredients_found(self, mock_get):
        mock_response = { 'hints': [] }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No substitude ingredients found")

    @patch('substitutionIngredients.views.requests.get')
    def test_error_api(self, mock_get):
        mock_get.side_effect = Exception("Error")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error")

            
        
