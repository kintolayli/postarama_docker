from allauth.account.views import LoginView, LogoutView, SignupView
from django.urls import path

from . import views

urlpatterns = [
    path("/accounts/login/", views.LoginView.as_view(), name="account_login"),
    path("/accounts/signup/", views.SignupView.as_view(), name="account_signup"),
    path("/accounts/logout/", views.LogoutView.as_view(), name="account_logout"),
]
