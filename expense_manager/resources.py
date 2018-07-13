# core django
from django.contrib.auth.models import User

# project
from .models import Expense

# third party
from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie.authorization import DjangoAuthorization

# tastypie task resource


class UserAuthorization(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)


class ExpenseResource(ModelResource):
    class Meta:
        queryset = Expense.objects.all()
        resource_name = 'expense'
        authorization = UserAuthorization()
        filtering = {
            'created': ['exact', 'range', 'gte'],
            'price': ALL
        }
        excludes = ('modified')