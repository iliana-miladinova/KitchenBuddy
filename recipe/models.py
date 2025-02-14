from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ingredients.models import Ingredient
from foodPreference.models import Allergy, Diet

# Create your models here.
DISH_TYPE = [('breakfast', 'breakfast'), ('starter', 'starter'),
             ('main', 'main'), ('dessert', 'dessert')]


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe")
    title = models.CharField(max_length=150)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientsDetails', related_name='recipe_ingredient')
    description = models.TextField()
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    calories = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2000)], null=True, blank=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    dish_type = models.CharField(max_length=10, choices=DISH_TYPE, default='main', null=False)

    favourite = models.ManyToManyField(User, related_name='favourite_recipe', blank=True)


    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    ratings_count = models.PositiveBigIntegerField(default=0)

    diet = models.ManyToManyField(Diet, related_name='recipe_diet', blank=True)
    allergies = models.ManyToManyField(Allergy, related_name='recipe_allergies', blank=True)
    #image_url = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        ordering = ['title']
        unique_together = ['title', 'image']
    
    def __str__(self):
        return self.title

    def update_ratings(self):
        ratings = self.rating.all()

        if ratings:
            total_ratings_val = 0
            for rating in ratings:
                total_ratings_val+=rating.rating_val

            self.ratings_count=len(ratings)
            self.average_rating = total_ratings_val/self.ratings_count
        else:
            self.ratings_count=0
            self.average_rating=0
        
        self.save()
            
class IngredientsDetails(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    amount = models.CharField(max_length=10) #mg, ml , etc

    class Meta:
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity} {self.amount}"


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="rating")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_val = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.recipe.update_ratings()
    
    class Meta:
        unique_together = ['recipe', 'user']


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.TextField()

    def __str__(self):
        return f"{self.user.username}: "