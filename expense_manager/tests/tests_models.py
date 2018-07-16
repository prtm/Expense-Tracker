# stdlib
from datetime import date
from decimal import Decimal

# core django
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
# Create your tests here.

# project
from expense_manager.models import Budget, Expense


class ExpenseMethodTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setting up non-modified objects used by all test methods
        user = User.objects.create_user(username='test_user')
        Expense.objects.create(user=user, name='Trip to pyconf', price=10000)
        Budget.objects.create(user=user, budget=25000.27)

    def test_name_label(self):
        expense = Expense.objects.get(id=1)
        field_label = expense._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        expense = Expense.objects.get(id=1)
        max_length = expense._meta.get_field('name').max_length
        self.assertEquals(max_length, 72)

    def test_name_max_digits(self):
        expense = Expense.objects.get(id=1)
        max_digits = expense._meta.get_field('price').max_digits
        decimal_places = expense._meta.get_field('price').decimal_places
        self.assertEquals(max_digits, 8)
        self.assertEquals(decimal_places, 2)

    def test_get_budget(self):
        expense = Expense.objects.get(id=1)
        budget_this_month = expense.get_budget
        self.assertEquals(budget_this_month, Decimal(
            25000.27).quantize(Decimal('0.01')))

    def test_object_name_is_username_comma_expensename_comma_(self):
        expense = Expense.objects.get(id=1)
        expected_object_name = '%s, %s, %f' % (
            expense.user, expense.name, expense.price)
        self.assertEquals(expected_object_name, str(expense))


class BudgetMethodTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setting up non-modified objects used by all test methods
        user = User.objects.create_user(username='test_user')
        Budget.objects.create(user=user, budget=35000.21)

    def test_budget_max_digits(self):
        budget = Budget.objects.get(id=1)
        max_digits = budget._meta.get_field('budget').max_digits
        decimal_places = budget._meta.get_field('budget').decimal_places
        self.assertEquals(max_digits, 8)
        self.assertEquals(decimal_places, 2)

    def test_default_month_year(self):
        budget = Budget.objects.get(id=1)
        self.assertEquals(budget.month, date.today().month)
        self.assertEquals(budget.year, date.today().year)

    def test_object_name_is_username_comma_expensename_comma_(self):
        budget = Budget.objects.get(id=1)
        expected_object_name = '%d-%d' % (budget.month, budget.year)
        self.assertEquals(expected_object_name, str(budget))

    def test_min_max_month(self):
        user2 = User.objects.create(username='test_user2')
        with self.assertRaises(ValidationError):
            Budget.objects.create(user=user2, budget=2345, month=13)

        with self.assertRaises(ValidationError):
            Budget.objects.create(user=user2, budget=2345, month=0)

        user3 = User.objects.create(username='test_user3')
        budget3 = Budget.objects.create(user=user3, budget=2345, month=11)
        self.assertEquals(budget3.month, 11)

    def test_min_max_year(self):
        user2 = User.objects.create(username='test_user2')
        with self.assertRaises(ValidationError):
            Budget.objects.create(user=user2, budget=2345, year=2036)

        with self.assertRaises(ValidationError):
            Budget.objects.create(user=user2, budget=2345, year=2014)

        user3 = User.objects.create(username='test_user3')
        budget3 = Budget.objects.create(user=user3, budget=2345, year=2018)
        self.assertEquals(budget3.year, 2018)
