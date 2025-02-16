from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from Users.models import Profile
from calorieTracker.models import CalorieTracker
from recipe.models import Recipe

class TestCalorieTrackerViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='iliana20', email='iliana@abv.bg', password='1234')
        self.client.login(username='iliana20', password='1234')
        self.profile = Profile.objects.create(user=self.user, calories=2500)
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
        #self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'calorieTracker/list_calorie_tracker.html')
        self.assertEqual(response.context['calorie_limit'], 2000)

    def test_list_calorie_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login')
        
        
        
        
