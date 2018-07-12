from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include(('expense_manager.urls','expense_manager'),namespace='expense_manager')),
]
