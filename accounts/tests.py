from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")

    def test_register_view(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'strongpassword',
            'password2': 'strongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Проверяем, что регистрация работает

    def test_login_view(self):
        response = self.client.post(reverse('accounts:login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Должно редиректить после успешного входа

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Проверяем, что выход срабатывает

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)  # Доступ к профилю
