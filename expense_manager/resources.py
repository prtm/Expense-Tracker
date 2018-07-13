# core django
from django.contrib.auth.models import User

# project
from .models import Expense

# third party
from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

# tastypie user authorization


# class UserAuthorization(DjangoAuthorization):
#     def read_list(self, object_list, bundle):
#         return object_list.filter(user=bundle.request.user)

#     def update_list(self, object_list, bundle):
#         allowed = []
#         print(object_list)
#         # Since they may not all be saved, iterate over them.
#         for obj in object_list:
#             if obj.user == bundle.request.user:
#                 allowed.append(obj)

#         return allowed


class ExpenseResource(ModelResource):
    # photo = fields.FileField(attribute="photo", null=True, blank=True)
    class Meta:
        queryset = Expense.objects.all()
        resource_name = 'expense'
        authorization = DjangoAuthorization()
        filtering = {
            'created': ['exact', 'range', 'gte'],
            'price': ALL
        }

        excludes = ('id', 'created', 'modified')

    def get_object_list(self, request):
        return super(ExpenseResource, self).get_object_list(request).filter(user=request.user)

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle
