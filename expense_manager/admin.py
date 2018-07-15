# core django
from django.contrib import admin
from django.db.models import Q
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

# project related
from .models import Expense, Budget


class ImageFilter(admin.SimpleListFilter):
    title = u'Image'

    parameter_name = u'photo'

    def lookups(self, request, model_admin):
        return (
            ('1', 'has image', ),
            ('0', 'no image', ),
        )

    def queryset(self, request, queryset):
        check_null = {
            '%s' % self.parameter_name: None,
        }
        check_blank = {
            '%s' % self.parameter_name: '',
        }
        if self.value() == '1':
            return queryset.exclude(Q(**check_null) | Q(**check_blank))
        if self.value() == '0':
            return queryset.filter(Q(**check_null) | Q(**check_blank))


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'price', 'created', 'modified')
    list_filter = ('created', 'modified', ImageFilter)
    search_fields = ('user__username', 'name', 'price')
    ordering = ('-modified', '-created')

    def photo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.headshot.url,
            width=obj.headshot.width,
            height=obj.headshot.height,))


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget', 'month', 'year', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('user__username', 'budget', 'month','year')
    ordering = ('-modified', '-created')
