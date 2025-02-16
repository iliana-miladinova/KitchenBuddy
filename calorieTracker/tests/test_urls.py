from django.test import SimpleTestCase
from django.urls import reverse, resolve
from calorieTracker.views import list_calorie_tracker, add_to_calorie_tracker, remove_from_calorie_tracker, edit_servings

class TestIngredientsUrls(SimpleTestCase):
    def test_list_calorie_tracker(self):
        url = reverse('list_calorie_tracker')
        self.assertEqual(resolve(url).func, list_calorie_tracker)

    def test_add_to_calorie_tracker(self):
        url = reverse('add_to_calorie_tracker', args=['1'])
        self.assertEqual(resolve(url).func, add_to_calorie_tracker)

    def test_remove_from_calorie_tracker(self):
        url = reverse('remove_from_calorie_tracker', args=['1'])
        self.assertEqual(resolve(url).func, remove_from_calorie_tracker)

    def test_edit_servings(self):
        url = reverse('update_servings', args=['1'])
        self.assertEqual(resolve(url).func, edit_servings)
