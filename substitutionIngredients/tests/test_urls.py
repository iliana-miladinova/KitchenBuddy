from django.test import SimpleTestCase
from django.urls import reverse, resolve
from substitutionIngredients.views import get_substitute_ingredients

class TestSubstitutionIngredientsUrls(SimpleTestCase):
    def test_get_substitute_ingredients_url_is_resolved(self):
        url = reverse('show_substitutes', args=[3, 1])
        self.assertEqual(resolve(url).func, get_substitute_ingredients)
