from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.user = User.objects.create_user(username='iliana20', email='iliana20@gmail.com', password='1234')

    def test_index_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_index_view_logged_in(self):
        self.client.login(username='iliana20', password='1234')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/welcome.html')