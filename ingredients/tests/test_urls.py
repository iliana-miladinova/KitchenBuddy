from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ingredients.views import get_recipes_by_ingredients

class TestIngredientsUrls(SimpleTestCase):
    def test_get_recipes_by_ingredients_url_is_resolved(self):
        url = reverse('get_recipes_by_ingredients')
        self.assertEqual(resolve(url).func, get_recipes_by_ingredients)
