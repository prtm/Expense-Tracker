# core django
from django.test import TestCase

# project
from accounts.forms import UserRegistrationForm

# Create your tests here.


class ExpenseFormTest(TestCase):

    def test_form_labels(self):
        form = UserRegistrationForm()
        self.assertTrue(form.fields['username'].label ==
                        None or form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['email'].label ==
                        None or form.fields['email'].label == 'Email')
        self.assertTrue(form.fields['password'].label ==
                        None or form.fields['password'].label == 'Password')

    def test_validation(self):
        email = 'test@gmail'
        username = 'test'
        password = '12345'
        form_data = {'email': email,
                     'username': username, 'password': password}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
