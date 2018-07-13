from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('accounts.urls','accounts'),namespace='accounts')),
    path('', include(('expense_manager.urls', 'expense_manager'),
                     namespace='expense_manager')),
    re_path(r'^$', lambda r: HttpResponseRedirect(reverse('login'))),
]
