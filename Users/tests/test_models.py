from django.test import TestCase
from Users.models import Profile
from django.contrib.auth.models import User

class TestUsersProfieModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Iliana20',
            email='iliana@abv.bg',
            password='Iliana123'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            age=20,
            gender='Female',
            weight=53,
            height=167,
            activity='moderate',
            calories=2035
        )

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.age, 20)
        self.assertEqual(self.profile.gender, 'Female')
        self.assertEqual(self.profile.weight, 53)
        self.assertEqual(self.profile.height, 167)
        self.assertEqual(self.profile.activity, 'moderate')
        self.assertEqual(self.profile.calories, 2035)

    def test_profile_str_rep(self):
        str_profile = f"This is {self.user.username}'s Profile"
        self.assertEqual(str(self.profile), str_profile)

    def test_profile_null_fields(self):
        empty_profile_user = User.objects.create_user(
            username='iliana',
            email='im@abv.bg',
            password='88888'
        )

        empty_profile = Profile.objects.create(user=empty_profile_user)
        self.assertEqual(empty_profile.age, None)
        self.assertEqual(empty_profile.gender, '')
        self.assertEqual(empty_profile.weight, None)
        self.assertEqual(empty_profile.height, None)
        self.assertEqual(empty_profile.activity, '')
        self.assertEqual(empty_profile.calories, None)  

    def test_profile_update(self):
        self.profile.age = 21
        self.profile.weight = 55
        self.profile.activity = 'light'
        
        self.profile.save()

        updated_profile = Profile.objects.get(user=self.user)

        self.assertEqual(updated_profile.age, 21)
        self.assertEqual(updated_profile.weight, 55)
        self.assertEqual(updated_profile.activity, 'light')

    def test_profile_user_deletion_cascade(self):
        self.assertEqual(Profile.objects.count(), 1)

        self.user.delete()

        self.assertEqual(Profile.objects.count(), 0)
        
        
