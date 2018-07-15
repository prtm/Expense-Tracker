# core django
from django.contrib.auth.models import User

# project
from .models import Expense, Budget

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

class BudgetResource(ModelResource):
    class Meta:
        queryset = Budget.objects.all()
        resource_name = 'budget'
        authorization = DjangoAuthorization()
        filtering = {
            'budget': ALL,
            'month': ALL,
        }
        ordering = ['month']
        excludes = ('id', 'created' 'modified')

    # filter obj for logged in user
    def get_object_list(self, request):
        return super(BudgetResource, self).get_object_list(request).filter(user=request.user)

    # store obj based on logged in
    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle
    # get detail obj direct

    def render_detail(self, request, pk):
        resp = self.get_detail(request, pk=pk)
        return resp.content
    # get list direct

    def render_list(self, request):
        resp = self.get_list(request)
        return resp.content


class ExpenseResource(ModelResource):
    # photo = fields.FileField(attribute="photo", null=True, blank=True)
    class Meta:
        queryset = Expense.objects.all()
        resource_name = 'expense'
        authorization = DjangoAuthorization()
        filtering = {
            'name': ALL,
            'price': ALL,
            'photo': ALL,
            'created': ['exact', 'range', 'gte']
        }
        ordering = ['name','price']
        excludes = ('id', 'modified')

    # filter obj for logged in user
    def get_object_list(self, request):
        return super(ExpenseResource, self).get_object_list(request).filter(user=request.user)

    # store obj based on logged in
    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle
    # get detail obj direct

    def render_detail(self, request, pk):
        resp = self.get_detail(request, pk=pk)
        return resp.content
    # get list direct

    def render_list(self, request):
        resp = self.get_list(request)
        return resp.content

    # https://github.com/django-tastypie/django-tastypie/issues/524
    # has image --> check if image blank --> ne filter required

    def build_filters(self, filters=None):
        """
        First, separate out normal filters and the __ne operations
        """
        if not filters:
            return filters

        applicable_filters = {}

        # Normal filtering
        filter_params = dict([(x, filters[x]) for x in filter(
            lambda x: not x.endswith('__ne'), filters)])
        applicable_filters['filter'] = super(
            type(self), self).build_filters(filter_params)

        # Exclude filtering
        exclude_params = dict([(x[:-4], filters[x])
                               for x in filter(lambda x: x.endswith('__ne'), filters)])
        applicable_filters['exclude'] = super(
            type(self), self).build_filters(exclude_params)

        return applicable_filters

    def apply_filters(self, request, applicable_filters):
        """
        Distinguish between normal filters and exclude filters
        """
        objects = self.get_object_list(request)

        f = applicable_filters.get('filter')
        if f:
            objects = objects.filter(**f)
        e = applicable_filters.get('exclude')
        if e:
            for exclusion_filter, value in e.items():
                objects = objects.exclude(**{exclusion_filter: value})
        return objects
