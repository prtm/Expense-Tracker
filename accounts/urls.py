# core django
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
# project
from .views import register, dashboard


urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard')
]
