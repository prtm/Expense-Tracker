# core django
from django.urls import path, reverse_lazy

# project
from .views import dashboard


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
]
