from django.test import TestCase
from recipe.forms import IngredientsDetailsForm
from recipe.models import IngredientsDetails
from ingredients.models import Ingredient

class TestIngredientsDetailsForm(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Tomato', category='vegetables')
        self.ingredient2 = Ingredient.objects.create(name='Strawberry', category='fruits')

    def test_form_valid(self):
        data = {
            'ingredient': self.ingredient.id,
            'quantity': 8,
            'amount': 'kg'
        }

        form = IngredientsDetailsForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        data = {
            'ingredient': self.ingredient.id,
            'quantity': -8,
            'amount': 'kg'
        }

        form = IngredientsDetailsForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_form_queryset_ingredients(self):
        form = IngredientsDetailsForm()
        queryset = form.fields['ingredient'].queryset

        self.assertEqual(list(queryset), list(Ingredient.objects.all().order_by('category', 'name')))

        self.assertIn(self.ingredient, queryset)
        self.assertIn(self.ingredient2, queryset)
