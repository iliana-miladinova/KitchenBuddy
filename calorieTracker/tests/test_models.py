from django.test import TestCase
from django.contrib.auth.models import User
from recipe.models import Recipe
from calorieTracker.models import CalorieTracker


class TestCalorieTrackerModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='iliana20', email='iliana@abv.bg', password='1234')
        self.recipe = Recipe.objects.create(user=self.user, title = 'my_recipe', calories=300)
        self.calorie_tracker = CalorieTracker.objects.create(user=self.user, recipe=self.recipe, servings=3)
        self.recipe2 = Recipe.objects.create(user=self.user, title='a_recipe', calories=200)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            CalorieTracker.objects.create(user=self.user, recipe=self.recipe)

    def test_get_calories_per_recipe(self):
        self.assertEqual(self.calorie_tracker.get_calories_per_recipe, 900)

    def test_get_total_calories(self):
        CalorieTracker.objects.create(user=self.user, recipe=self.recipe2, servings=8)
        sum_calories = CalorieTracker.get_total_calories(self.user)
        self.assertEqual(sum_calories, 2500)

    



        
        
