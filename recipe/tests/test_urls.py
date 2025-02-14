from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recipe.views import list_recipe, recipe_create, favourite_recipes
from recipe.views import add_remove_favourite, recipe_details, recipe_update, add_rating
from recipe.views import add_comment, get_menu, recipe_create


class TestRecipeUrls(SimpleTestCase):
    def test_list_recipe_url_is_resolved(self):
        url = reverse('list_recipe')
        self.assertEqual(resolve(url).func, list_recipe)

    def test_recipe_create_url_is_resolved(self):
        url = reverse('recipe_create')
        self.assertEqual(resolve(url).func, recipe_create)

    def test_favourite_recipes_url_is_resolved(self):
        url = reverse('favourite_recipes')
        self.assertEqual(resolve(url).func, favourite_recipes)

    def test_add_remove_favourite_url_is_resolved(self):
        url = reverse('add_remove_favourite', args=[3])
        self.assertEqual(resolve(url).func, add_remove_favourite)

    def test_recipe_details_url_is_resolved(self):
        url = reverse('recipe_details', args=[3])
        self.assertEqual(resolve(url).func, recipe_details)

    def test_recipe_update_url_is_resolved(self):
        url = reverse('recipe_update', args=[3])
        self.assertEqual(resolve(url).func, recipe_update)

    def test_add_rating_url_is_resolved(self):
        url = reverse('add_rating', args=[3])
        self.assertEqual(resolve(url).func, add_rating)

    def test_add_comment_url_is_resolved(self):
        url = reverse('add_comment', args=[3])
        self.assertEqual(resolve(url).func, add_comment)

    def test_get_menu_url_is_resolved(self):
        url = reverse('get_menu')
        self.assertEqual(resolve(url).func, get_menu)

    
        
        
