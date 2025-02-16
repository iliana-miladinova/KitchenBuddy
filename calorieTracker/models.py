from django.db import models
from recipe.models import Recipe
from django.contrib.auth.models import User

# Create your models here.
class CalorieTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    servings = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['user', 'recipe']

    @property
    def get_calories_per_recipe(self):
        return self.recipe.calories * self.servings
    
    @classmethod
    def get_total_calories(cls, user):
        recipes_in_tracker = cls.objects.filter(user=user)
        calories_sum = 0
        
        for recipe in recipes_in_tracker:
            calories_sum += recipe.get_calories_per_recipe
        
        return calories_sum
