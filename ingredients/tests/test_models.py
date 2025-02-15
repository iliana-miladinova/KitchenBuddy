from django.test import TestCase
from ingredients.models import Ingredient

class TestIngredientModel(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='my_ingredient', category='vegetables')
        self.ingredient2 = Ingredient.objects.create(name='my_ingredient2', category='fruits')

    def test_ingredient_creation(self):
        self.assertTrue(isinstance(self.ingredient, Ingredient))
        self.assertEqual(self.ingredient.name, 'my_ingredient')
        self.assertEqual(self.ingredient.category, 'vegetables')

    def test_ingredient_str_rep(self):
        str_ingredient = f"{self.ingredient.name}"
        self.assertEqual(str(self.ingredient), str_ingredient)

    def test_ingredient_ordering(self):
        ingredients = Ingredient.objects.all()
        self.assertEqual(ingredients[0], self.ingredient2)
        self.assertEqual(ingredients[1], self.ingredient)

    def test_ingredient_unique_name(self):
        with self.assertRaises(Exception):
            Ingredient.objects.create(name='my_ingredient', category='vegetables')
        
        
        
