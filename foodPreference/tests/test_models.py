from django.test import TestCase
from foodPreference.models import Diet, Allergy

class TestDietModel(TestCase):
    def setUp(self):
        self.diet = Diet.objects.create(name='MyDiet')
    
    def test_diet_creation(self):
        self.assertTrue(isinstance(self.diet, Diet))
        self.assertEqual(self.diet.name, 'MyDiet')

    def test_diet_str_rep(self):
        str_diet = self.diet.name
        self.assertEqual(str(self.diet), str_diet)

    def test_diet_unique_name(self):
        with self.assertRaises(Exception):
            Diet.objects.create(name='MyDiet')

class TestAllergyModel(TestCase):
    def setUp(self):
        self.allergy = Allergy.objects.create(name='MyAllergy')

    def test_allergy_creation(self):
        self.assertTrue(isinstance(self.allergy, Allergy))
        self.assertEqual(self.allergy.name, 'MyAllergy')

    def test_allergy_str_rep(self):
        str_allergy = self.allergy.name
        self.assertEqual(str(self.allergy), str_allergy)

    def test_allergy_unique_name(self):
        with self.assertRaises(Exception):
            Allergy.objects.create(name='MyAllergy')

    
    


