# core django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.


class UserViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test', email='test@gmail.com', password='12345')

    def test_login_url(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_register_url(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

    def test_login_url_accessible_by_name(self):
        resp = self.client.get(
            reverse('accounts:login'))
        self.assertEqual(resp.status_code, 200)
    
    def test_register_url_accessible_by_name(self):
        resp = self.client.get(
            reverse('accounts:register'))
        self.assertEqual(resp.status_code, 200)

    def test_login_success(self):
        self.client.login(username='test', password='12345')
        resp = self.client.get(
            reverse('expense_manager:dashboard'))
        self.assertEqual(str(resp.context['user']), 'test')
    
    def test_unauthenticated_access(self):
        resp = self.client.get(
            reverse('expense_manager:dashboard'))
        self.assertEqual(resp.status_code, 302)

    def test_login_authenticated_redirect(self):
        self.client.login(username='test', password='12345')
        resp = self.client.get(
            reverse('accounts:login'))
        self.assertEqual(resp.status_code, 302)

