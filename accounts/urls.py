# core django
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordChangeView, PasswordChangeDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# project
from .views import register


urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    path('register/', register, name='register'),
]
