# stdlib
import json
# core django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# project related
from expense_manager.models import Expense


# third-party
# from tastypie.test import ResourceTestCaseMixin

# Create your tests here.


class ExpenseListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test', email='test@gmail.com', password='12345')

    def test_dashboard_url(self):
        login = self.client.login(username='test', password='12345')
        resp = self.client.get('/dashboard/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_url_accessible_by_name(self):
        self.client.login(username='test', password='12345')
        resp = self.client.get(
            reverse('expense_manager:dashboard'), follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_no_image_found(self):
        self.client.login(username='test', password='12345')
        resp = self.client.get(
            reverse('expense_manager:image_uploader'), follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_dashboard_template_found(self):
        self.client.login(username='test', password='12345')
        resp = self.client.get('/dashboard/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'expense_manager/dashboard/dashboard.html')

# class ExpenseApiTest(ResourceTestCaseMixin, TestCase):
        # setUp(self):

    # def test_pagination_limit(self):
    #     self.client.login(username='test', password='12345')
    #     resp = self.client.get('/api/v1/expense/',follow=True)
    #     self.assertEqual(resp.status_code, 200)
    #     response_dict = json.loads(str(resp.content, encoding='utf8'))
    #     self.assertTrue('meta' in response_dict)
    #     self.assertTrue('objects' in response_dict)
    #     self.assertTrue(len(response_dict['objects']) == 20)

    # def test_lists_all_expenses(self):
    #     self.client.login(username='test', password='12345')
    #     resp = self.client.get('/api/v1/expense/?offset=20',follow=True)
    #     self.assertEqual(resp.status_code, 200)
    #     response_dict = json.loads(str(resp.content, encoding='utf8'))
    #     self.assertTrue('meta' in response_dict)
    #     self.assertTrue('objects' in response_dict)
    #     self.assertTrue(len(response_dict['objects']) == 5)

