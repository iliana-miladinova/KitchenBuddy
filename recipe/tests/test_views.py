from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from recipe.models import Recipe, IngredientsDetails, Rating, Comment
from ingredients.models import Ingredient
from django.core.files.uploadedfile import SimpleUploadedFile
from foodPreference.models import Diet, Allergy
from Users.models import Profile

class TestListRecipeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')
        self.url = reverse('list_recipe')

        self.diet = Diet.objects.create(name='my_diet')
        self.allergy = Allergy.objects.create(name='my_allergy')
        self.image = SimpleUploadedFile(name='food_image.jpg', content=b'file_content', content_type='image/jpeg')

        self.ingredient1 = Ingredient.objects.create(name="Tomato", category="Vegetables")
        self.ingredient2 = Ingredient.objects.create(name="Cheese", category="Dairy")

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='a_recipe',
            description='my_description',
            cooking_time=80,
            calories=333,
            dish_type='main',
            image=self.image
        )

        IngredientsDetails.objects.create(recipe=self.recipe, ingredient=self.ingredient1, quantity=3, amount='grama')
        IngredientsDetails.objects.create(recipe=self.recipe, ingredient=self.ingredient2, quantity=8, amount='kg')
        
        self.recipe.diet.add(self.diet)
        self.recipe.allergies.add(self.allergy)

        self.recipe2 = Recipe.objects.create(
            user=self.user,
            title='my_recipe2',
            description='my_description2',
            cooking_time=60,
            calories=111,
            dish_type='dessert',
            image=self.image
        )

        IngredientsDetails.objects.create(recipe=self.recipe2, ingredient=self.ingredient2, quantity=8, amount='kg')


    def test_list_recipe_authenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/list_recipe.html')

    def test_list_recipe_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url) 
        
    def test_sort_by_calories(self):
        response = self.client.get(self.url, {'sort_by': 'calories'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['all_recipes']), [self.recipe2, self.recipe])

    def test_sort_by_cooking_time(self):
        response = self.client.get(self.url, {'sort_by': 'cooking_time'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['all_recipes']), [self.recipe2, self.recipe])
    
    def test_sort_by_title(self):
        response = self.client.get(self.url, {'sort_by': 'title'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['all_recipes']), [self.recipe, self.recipe2])

    def test_filter_by_diet(self):
        response = self.client.get(self.url, {'diets_filter': self.diet.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['all_recipes']), [self.recipe])

    def test_filter_by_allergy(self):
        response = self.client.get(self.url, {'allergies_filter': self.allergy.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['all_recipes']), [self.recipe2])


class TestCreateRecipeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')
        self.url = reverse('recipe_create')

        self.diet = Diet.objects.create(name='my_diet')
        self.allergy = Allergy.objects.create(name='my_allergy')
        self.image = SimpleUploadedFile(name='food_image.jpg', content=b'file_content', content_type='image/jpeg')

        self.ingredient1 = Ingredient.objects.create(name="Tomato", category="Vegetables")
        self.ingredient2 = Ingredient.objects.create(name="Cheese", category="Dairy")

    def test_create_recipe_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/create_recipe.html')

    def test_create_recipe_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_create_recipe_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/create_recipe.html')
        self.assertIn('ingredients', response.context)
        self.assertIn('diets', response.context)
        self.assertIn('allergies', response.context)
        self.assertIn('ingredients_form', response.context)


class TestFavouriteRecipeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')
        
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

        self.url = reverse('add_remove_favourite', args=[self.recipe.id])

    def test_add_to_favourite(self):
        response = self.client.post(self.url)

        self.assertIn(self.user, self.recipe.favourite.all())
        self.assertRedirects(response, reverse('recipe_details', args=[self.recipe.id]))

    def test_remove_from_favourite(self):
        self.recipe.favourite.add(self.user)
        response = self.client.post(self.url)

        self.assertNotIn(self.user, self.recipe.favourite.all())
        self.assertRedirects(response, reverse('recipe_details', args=[self.recipe.id]))

class TestFavouriteRecipeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')

        self.image = SimpleUploadedFile(name='food_image.jpg', content=b'file_content', content_type='image/jpeg')

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
        )

        self.recipe2 = Recipe.objects.create(
            user=self.user,
            title='my_recipe2',
            description='my_description2',
            cooking_time=60,
            calories=111,
        )

        self.recipe.favourite.add(self.user)

        self.url = reverse('favourite_recipes')
    
    def test_favourite_recipes_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/favourite_recipes.html')

        favourite_recipes = response.context['favourite_recipes']
        self.assertIn(self.recipe, favourite_recipes)
        self.assertNotIn(self.recipe2, favourite_recipes)

class TestRecipeDetailsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
        )

        self.url = reverse('recipe_details', args=[self.recipe.id])

        self.ingredient1 = Ingredient.objects.create(name="Tomato", category="Vegetables")
        self.ingredient_details = IngredientsDetails.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient1,
            quantity=300,
            amount='grama'
        )

    def test_recipe_details_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_details.html')

        self.assertEqual(response.context['recipe'], self.recipe)
        self.assertIn(self.ingredient_details, response.context['ingredients'])


class TestRecipeUpdateViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
        )

        self.url = reverse('recipe_update', args=[self.recipe.id])

    def test_update_view_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_update.html')

        
class TestAddRatingViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60,
            calories=111,
        )

        self.url = reverse('add_rating', args=[self.recipe.id])
    
    def test_add_rating(self):
        response = self.client.post(self.url, {'rating': 3})

        rating = Rating.objects.get(recipe=self.recipe, user=self.user)

        self.assertEqual(rating.rating_val, 3)
        self.assertRedirects(response, reverse('recipe_details', args=[self.recipe.id]))


class TestAddCommentViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')

        self.recipe = Recipe.objects.create(
            user=self.user,
            title='my_recipe',
            description='my_description',
            cooking_time=60
        )

        self.url = reverse('add_comment', args=[self.recipe.id])
    
    def test_add_comment(self):
        comment_text = {'comment': 'my_comment'}
        response = self.client.post(self.url, comment_text)

        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(comment.comment, 'my_comment')
        self.assertRedirects(response, reverse('recipe_details', args=[self.recipe.id]))

class TestGetMenuView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')
        self.client.login(username='iliana20', password='1234')
        
        self.profile = Profile.objects.create(user=self.user, calories=2034)
        
        self.breakfast = Recipe.objects.create(
            user=self.user,
            title='my_breakfast',
            description='1234',
            cooking_time=15,
            calories=400,  
            dish_type='breakfast'
        )

        self.starter = Recipe.objects.create(
            user=self.user,
            title='my_starter',
            description='1234',
            cooking_time=20,
            calories=150,
            dish_type='starter'
        )
        
        self.main = Recipe.objects.create(
            user=self.user,
            title='my_ain',
            description='1234',
            cooking_time=45,
            calories=400, 
            dish_type='main'
        )

        self.dessert = Recipe.objects.create(
            user=self.user,
            title='my_dessert',
            description='1234',
            cooking_time=30,
            calories=80, 
            dish_type='dessert'
        )
        
        # Добавяме всички рецепти в любими
        for recipe in [self.breakfast, self.starter, self.main, self.dessert]:
            recipe.favourite.add(self.user)
        
        self.url = reverse('get_menu')

    def test_get_menu(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/get_menu.html')
        
        menu = response.context['menu']
        
        self.assertIsNotNone(menu['breakfast'])
        self.assertIsNotNone(menu['lunch']['starter'])
        self.assertIsNotNone(menu['lunch']['main'])
        self.assertIsNotNone(menu['lunch']['dessert'])
        self.assertIsNotNone(menu['dinner']['starter'])
        self.assertIsNotNone(menu['dinner']['main'])
        self.assertIsNotNone(menu['dinner']['dessert'])
        
        total_calories = response.context['total_calories_menu']
        self.assertLessEqual(total_calories, 2034)

        self.assertEqual(response.context['recommended_calories'], 2034)