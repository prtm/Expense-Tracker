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
    month = models.PositiveSmallIntegerField(default=date.today().month, validators=[
        MaxValueValidator(12), MinValueValidator(1)])
    year = models.PositiveSmallIntegerField(default=date.today().year, validators=[
        MaxValueValidator(2035), MinValueValidator(2015)])

    def save(self, *args, **kwargs):
        if self.month >= 1 and self.month <= 12 and self.year >= 2015 and self.year <= 2035:
            super(Budget, self).save(*args, **kwargs)
        else:
            raise ValidationError('Incorrect Month or Year')

    class Meta:
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return '%d-%d' % (self.month, self.year)


class UserExpenseQuerySet(models.QuerySet):
    def all_expenses(self, user):
        return self.filter(user=user).order_by('-created')

    def total_expense(self, user, month, year):
        return self.filter(user=user, created__month=month, created__year=year).aggregate(total_expense=models.Sum('price'))

    def top_10_month_expenses(self, user, month, year):
        return self.filter(user=user, created__month=month, created__year=year).order_by('-price')[:10]


class UserExpensesManager(models.Manager):
    def get_queryset(self):
        return UserExpenseQuerySet(self.model, using=self._db)

    def all_expenses(self, user):
        return self.get_queryset().all_expenses(user)

    def total_expense(self, user, month, year):
        return self.get_queryset().total_expense(user, month, year)

    def top_10_month_expenses(self, user, month, year):
        return self.get_queryset().top_10_month_expenses(user, month, year)


class Expense(TimeStampedModel):
    user = models.ForeignKey(User, related_name='expenses',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=72)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='', null=True, blank=True)
    objects = models.Manager()
    manager = UserExpensesManager()

    @property
    def get_budget(self):
        budget = self.user.budget.filter(month=self.created.month)
        return budget[0].budget if budget else None

    def __str__(self):
        return '%s, %s, %f' % (self.user, self.name, self.price)
    
    class Meta:
        ordering = ('-created',)
