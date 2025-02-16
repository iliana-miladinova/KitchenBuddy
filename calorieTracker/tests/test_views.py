from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from Users.models import Profile
from calorieTracker.models import CalorieTracker
from recipe.models import Recipe

class TestCalorieTrackerViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='iliana20', email='iliana@abv.bg', password='1234')
        self.profile = Profile.objects.create(user=self.user, calories=2034)

        self.recipe = Recipe.objects.create(user=self.user, title = 'my_recipe', calories=300)

        self.calorie_tracker = CalorieTracker.objects.create(user=self.user, recipe=self.recipe, servings=3)

        self.client.login(username='iliana20', password='1234')

        self.url = reverse('list_calorie_tracker')

    
    def test_list_recipe_authenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        
    def test_list_calorie_tracker(self):
        response = self.client.get(self.url)
        #self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'calorieTracker/list_calorie_tracker.html')
        self.assertEqual(response.context['calories_sum'], 900)
        self.assertEqual(response.context['remaining_calories'], 1134)
        self.assertEqual(response.context['calorie_limit'], 2034)
        self.assertEqual(response.context['no_left_calories'], False)
        self.assertEqual(response.context['recipes_in_tracker'].count(), 1)

    def test_list_calorie_tracker_no_profile(self):
        self.profile.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calorieTracker/list_calorie_tracker.html')
        self.assertEqual(response.context['calorie_limit'], 2000)

    def test_list_calorie_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_add_to_calorie_tracker(self):
        recipe2 = Recipe.objects.create(user=self.user, title='a_recipe', calories=200)
        
        response = self.client.post(reverse('add_to_calorie_tracker', kwargs={'recipe_id': recipe2.id}))

        self.assertTrue(CalorieTracker.objects.filter(user=self.user, recipe=recipe2).exists())

        self.assertRedirects(response, reverse('list_calorie_tracker'))

    def test_remove_from_calorie_tracker(self):
        response = self.client.post(reverse('remove_from_calorie_tracker', kwargs={'recipe_id': self.recipe.id}))
        self.assertFalse(CalorieTracker.objects.filter(user=self.user, recipe=self.recipe).exists())
        self.assertRedirects(response, reverse('list_calorie_tracker'))

    def test_edit_servings(self):
        new_servings = 5
        response = self.client.post(reverse('update_servings', kwargs={'recipe_id': self.recipe.id}),
                                                            {'servings': new_servings})
        
        self.calorie_tracker.refresh_from_db()
        self.assertEqual(self.calorie_tracker.servings, new_servings)   
        self.assertRedirects(response, self.url) 


        
        
        
        
