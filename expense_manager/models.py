# core django
from django.db import models
from django.contrib.auth.models import User


# Timestamp model to add created and modified field
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Expense Model
class Expense(TimeStampedModel):
    user = models.ForeignKey(User, related_name='expenses',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='expense', null=True, blank=True)
