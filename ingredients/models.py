from django.db import models

# Create your models here.

class Ingredient(models.Model):
    INGREDIENT_CATEGORY = [('fruits', 'Fruits'), ('vegetables', 'Vegetables'), ('dairy', 'Dairy'), ('meat', 'Meat'), ('grains', 'Grains'), ('spices', 'Spieces')]

    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=INGREDIENT_CATEGORY)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category', 'name']

# class Substitute(models.Model):
#     ingredient=models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient')
#     substitute_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='substitude_ingrdient')

#     def __str__(self):
#         return f"{self.ingredient.name} can be replaced with {self.substitute_ingredient.name}"
    
#     class Meta:
#         ordering = ['ingredient__name', 'substitute_ingredient__name']
    