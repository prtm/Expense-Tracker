# stdlib
from datetime import date

# core django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


# Timestamp model to add created and modified field
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Budget(TimeStampedModel):
    user = models.ForeignKey(User, related_name='budget',
                             on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    month = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(12), MinValueValidator(1)])

    def save(self, *args, **kwargs):
        if self.month >= 1 and self.month <= 12:
            super(Budget, self).save(*args, **kwargs)
        else:
            raise ValidationError('Incorrect Month')

    class Meta:
        unique_together = ('user', 'month')


class UserExpenseQuerySet(models.QuerySet):
    def all_expenses(self, user):
        return self.filter(user=user).order_by('-created')

    def total_expense(self, user, month):
        return self.filter(user=user, created__month=month).aggregate(total_expense=models.Sum('price'))

    def top_10_month_expenses(self, user):
        return self.filter(user=user, created__month=date.today().month).order_by('-price')[:10]


class UserExpensesManager(models.Manager):
    def get_queryset(self):
        return UserExpenseQuerySet(self.model, using=self._db)

    def all_expenses(self, user):
        return self.get_queryset().all_expenses(user)

    def total_expense(self, user, month):
        return self.get_queryset().total_expense(user, month)

    def top_10_month_expenses(self, user):
        return self.get_queryset().top_10_month_expenses(user)


class Expense(TimeStampedModel):
    user = models.ForeignKey(User, related_name='expenses',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='media/', null=True, blank=True)
    objects = models.Manager()
    manager = UserExpensesManager()

    class Meta:
        ordering = ('-created',)

    @property
    def get_budget(self):
        budget = self.user.budget.filter(month=self.created.month)
        return budget if budget else ''
