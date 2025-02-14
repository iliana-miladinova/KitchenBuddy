from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main_app.views import index

class TestMainAppUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, index)
