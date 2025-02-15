from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from recipe.models import Recipe, Rating, IngredientsDetails, Comment
from ingredients.models import Ingredient
from foodPreference.models import Diet, Allergy

class TestRecipeModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.user2 = User.objects.create_user(username='marti', email='marti123@gmail.com', password='1234')

        self.image = SimpleUploadedFile(name='food_image.jpg', content=b'file_content', content_type='image/jpeg')

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
            dish_type='main',
            image=self.image
        )

        self.recipe2 = Recipe.objects.create(
            user=self.user,
            title='a_recipe',
            description='a_description',
            cooking_time=60,
            calories=111,
            dish_type='main',
            image=self.image
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.user, self.user)
        self.assertEqual(self.recipe.title, 'my_recipe')
        self.assertEqual(self.recipe.description, 'my_description')
        self.assertEqual(self.recipe.cooking_time, 60)
        self.assertEqual(self.recipe.calories, 111)
        self.assertEqual(self.recipe.dish_type, 'main')
        self.assertTrue(self.recipe.image)

    def test_recipe_str_rep(self):
        self.assertEqual(str(self.recipe), 'my_recipe')

    def test_ordering(self):
        recipes = Recipe.objects.all()
        self.assertEqual(recipes[0], self.recipe2)
        self.assertEqual(recipes[1], self.recipe)

    def test_update_ratings(self):
        Rating.objects.create(recipe=self.recipe, user=self.user, rating_val=5)
        Rating.objects.create(recipe=self.recipe, user=self.user2, rating_val=4)

        self.recipe.update_ratings()

        self.assertEqual(self.recipe.average_rating, 4.5)
        self.assertEqual(self.recipe.ratings_count, 2)

class TestIngredientsDetailsModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
            dish_type='main',
        )

        self.ingredient = Ingredient.objects.create(name='Tomato', category='vegetables')

        self.ingredient_details = IngredientsDetails.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=300,
            amount='grama'
        )

    def test_ingredient_details_creation(self):
        self.assertEqual(self.ingredient_details.recipe, self.recipe)
        self.assertEqual(self.ingredient_details.ingredient, self.ingredient)
        self.assertEqual(self.ingredient_details.quantity, 300)
        self.assertEqual(self.ingredient_details.amount, 'grama')

    def test_ingredient_details_str_rep(self):
        self.assertEqual(str(self.ingredient_details), 'Tomato - 300 grama')

    def test_delete_recipe_cascade(self):
        self.recipe.delete()
        self.assertEqual(IngredientsDetails.objects.count(), 0)

    def test_delete_ingredient_cascade(self):
        self.ingredient.delete()
        self.assertEqual(IngredientsDetails.objects.count(), 0)

class TestRatingModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.user2 = User.objects.create_user(username='marti', email='marti123@gmail.com', password='1234')

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
            dish_type='main',
        )

    def test_rating_creation(self):
        rating = Rating.objects.create(recipe=self.recipe, user=self.user, rating_val=3)

        self.assertEqual(rating.recipe, self.recipe)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.rating_val, 3)

    def test_delete_recipe_cascade(self):
        self.recipe.delete()
        self.assertEqual(Rating.objects.count(), 0)

    def test_delete_user_cascade(self):
        self.user.delete()
        self.assertEqual(Rating.objects.count(), 0)


class TestCommentModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
            dish_type='main',
        )
        
        self.comment = Comment.objects.create(recipe=self.recipe, user=self.user, 
                                              comment='Iliana is saying that this is the best ever')
        
    def test_comment_creation(self):
        self.assertEqual(self.comment.recipe, self.recipe)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.comment, 'Iliana is saying that this is the best ever')

    def test_delete_recipe_cascade(self):
        self.recipe.delete()
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_user_cascade(self):
        self.user.delete()
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_str_rep(self):
        self.assertEqual(str(self.comment), 'iliana20: Iliana is saying that this is the best ever')