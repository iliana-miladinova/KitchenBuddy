from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Users.models import Profile

class TestUsersRegisterView(TestCase):
    def setUp(self):
        self.url = reverse('register')

        self.data = {
            'username': 'Iliana20',
            'email': 'iliana@abv.bg',
            'password': 'Iliana123',
            'confirm_password': 'Iliana123'
        }

    def test_register_view_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/registration.html")

    def test_register_view_success(self):
        response = self.client.post(self.url, self.data)

        login_url = reverse('login')

        self.assertRedirects(response, login_url)

        self.assertTrue(User.objects.filter(username=self.data['username']).exists())

        user = User.objects.get(username=self.data['username'])
        self.assertEqual(user.email, self.data['email'])

        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Your account was created successfuly! Please, login.')

    def test_register_view_invalid_email(self):
        invalid_data = {
            'username': 'Iliana20',
            'email': 'iliana.email',
            'password': 'Iliana123',
            'confirm_password': 'Iliana123'
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/registration.html")
        self.assertContains(response, 'Invalid email format')
        self.assertFalse(User.objects.filter(username=self.data['username']).exists())

    def test_register_view_duplicate_email(self):
        User.objects.create_user(
            username='iliana_miladinova',
            email='iliana@abv.bg',
            password='iliana888'
        )

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/registration.html")
        self.assertContains(response, 'This email is already used')
        self.assertFalse(User.objects.filter(username=self.data['username']).exists())

    def test_register_view_passwords_mismatch(self):
        invalid_data = {
            'username': 'Iliana20',
            'email': 'iliana@abv.bg',
            'password': 'Iliana123',
            'confirm_password': 'Iliana*'
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/registration.html")
        self.assertContains(response, 'Passwords do not match')
        self.assertFalse(User.objects.filter(username=self.data['username']).exists())

    def test_register_view_duplicate_username(self):
        User.objects.create_user(
            username='Iliana20',
            email='iliana20@gmail.com',
            password='Iliana123'
        )

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/registration.html")
        self.assertContains(response, 'An acount with this username already exists')
        self.assertTrue(User.objects.filter(username=self.data['username']).count() == 1)


class TestUsersLoginView(TestCase):
    def setUp(self):
        self.url = reverse('login')

        self.user = User.objects.create_user(
            username='Iliana20',
            email='iliana@abv.bg',
            password='Iliana123'
        )

        self.data = {
            'username': 'Iliana20',
            'password': 'Iliana123'
        }
        
    def test_login_view_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/login.html")

    def test_login_view_success(self):
        response = self.client.post(self.url, self.data)

        home_url = reverse('home')
        self.assertRedirects(response, home_url)

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_login_view_invalid_password(self):
        invalid_data = {
            'username': 'Iliana20',
            'password': 'Iliana1234'
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/login.html")
        self.assertContains(response, 'Incorrect username or password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_invalid_username(self):
        invalid_data = {
            'username': 'IlianaMiladinova',
            'password': 'Iliana123'
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/login.html")
        self.assertContains(response, 'Incorrect username or password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_user_is_authenticated(self):
        self.client.login(username=self.data['username'], password=self.data['password'])
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('home'))


class TestUsersLogoutView(TestCase):
    def test_logout_view_success(self): 
        User.objects.create_user(
            username='Iliana20',
            email='iliana@abv.bg',
            password='Iliana123'
        )

        self.client.login(username='Iliana20', password='Iliana123')

        url = reverse('logout')
        response = self.client.get(url)

        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class TestUsersProfileView(TestCase):
    def setUp(self):
        self.url = reverse('profile')

        self.user = User.objects.create_user(
            username='Iliana20',
            email='iliana@abv.bg',
            password='Iliana123'
        )

        self.client.login(username='Iliana20', password='Iliana123')

        self.valid_data = {
            'age': 20,
            'gender': 'Female',
            'weight': 53,
            'height': 167,
            'activity': 'moderate'
        }

        self.valid_data_male = {
            'age': 20,
            'gender': 'Male',
            'weight': 72,
            'height': 178,
            'activity': 'moderate'
        }

    def test_profile_view_get_no_existing_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/profile.html")
        self.assertFalse(Profile.objects.filter(user=self.user).exists())

    def test_profile_view_get_existing_profile(self):
        profile = Profile.objects.create(
            user=self.user,
            age=self.valid_data['age'],
            gender=self.valid_data['gender'],
            weight=self.valid_data['weight'],
            height=self.valid_data['height'],
            activity=self.valid_data['activity'],
            calories=2035
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Users/profile.html")

        self.assertEqual(response.context['user_profile'], profile)

    def test_profile_view_create_profile(self):
        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.age, self.valid_data['age'])
        self.assertEqual(profile.gender, self.valid_data['gender'])
        self.assertEqual(profile.weight, self.valid_data['weight'])
        self.assertEqual(profile.height, self.valid_data['height'])
        self.assertEqual(profile.activity, self.valid_data['activity'])
        self.assertEqual(profile.calories, 2035)

    def test_profile_view_update_profile(self):
        Profile.objects.create(
            user=self.user,
            age=25,
            gender=self.valid_data['gender'],
            weight=self.valid_data['weight'],
            height=self.valid_data['height'],
            activity='light',
        )

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.age, self.valid_data['age'])
        self.assertEqual(profile.activity, self.valid_data['activity'])

    def test_profile_view_calculate_calories_female(self):
        response = self.client.post(self.url, self.valid_data)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.calories, 2035)

    def test_profile_view_calculate_calories_male(self):
        response = self.client.post(self.url, self.valid_data_male)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.calories, 2693)