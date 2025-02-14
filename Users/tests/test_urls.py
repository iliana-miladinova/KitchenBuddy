from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Users.views import register_view, login_view, logout_view, profile

class TestUsersUrls(SimpleTestCase):
    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register_view)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)
    
    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)
