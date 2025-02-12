from django.db import models
from ingredients.models import Ingredient

# Create your models here.
class Substitute(models.Model):
    ingredient=models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    substitute_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='substitude_ingrdient')

    def __str__(self):
        return f"{self.ingredient.name} can be replaced with {self.substitute_ingredient.name}"
    
    class Meta:
        ordering = ['ingredient__name', 'substitute_ingredient__name']
    