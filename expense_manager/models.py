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

    class Meta():
        unique_together = ('user', 'month')

# Expense Model


class Expense(TimeStampedModel):
    user = models.ForeignKey(User, related_name='expenses',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='expense', null=True, blank=True)

    # def get_budget(self):
