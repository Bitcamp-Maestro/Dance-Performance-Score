from django.urls import path
from . import views
from .views import UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name = "validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name = "validate_email")
]  