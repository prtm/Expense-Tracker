# std lib
from datetime import date

# core django
from django.test import TestCase

# project
from expense_manager.forms import ExpenseForm

# Create your tests here.
class ExpenseFormTest(TestCase):

    def test_form_labels(self):
        form = ExpenseForm()        
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Name')
        self.assertTrue(form.fields['price'].label == None or form.fields['price'].label == 'Price')
        self.assertTrue(form.fields['photo'].label == None or form.fields['photo'].label == 'Photo')