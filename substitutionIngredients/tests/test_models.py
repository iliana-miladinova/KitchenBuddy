from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ingredients.models import Ingredient
from substitutionIngredients.models import Substitute

class TestSubstituteModel(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name = 'Daisy', category = 'vegetables')
        self.ingredient2 = Ingredient.objects.create(name = 'Violet', category = 'vegetables')
        self.ingredient3 = Ingredient.objects.create(name = 'Lily', category = 'vegetables')

    def test_substitute_ingredient_creation(self):
        substitute = Substitute.objects.create(ingredient = self.ingredient, 
                                               substitute_ingredient = self.ingredient2)
        
        self.assertEqual(substitute.ingredient, self.ingredient)
        self.assertEqual(substitute.substitute_ingredient, self.ingredient2)

    def test_substitude_ingredients_str_rep(self):
        substitute = Substitute.objects.create(ingredient = self.ingredient, 
                                               substitute_ingredient = self.ingredient2)
        
        self.assertEqual(str(substitute), "Daisy can be replaced with Violet")

    def test_substitude_ingredients_ordering(self):
        Substitute.objects.create(ingredient = self.ingredient, 
                                  substitute_ingredient = self.ingredient2)
        Substitute.objects.create(ingredient = self.ingredient, 
                                  substitute_ingredient = self.ingredient3)
        
        substitutes = Substitute.objects.all()
        self.assertEqual(substitutes[0].ingredient, self.ingredient)
        self.assertEqual(substitutes[1].ingredient, self.ingredient)
        
        

        
