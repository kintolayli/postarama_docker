from django.urls import path
from allauth.account.views import LoginView, SignupView, LogoutView

from . import views

urlpatterns = [
    # path("signup/", views.SignUp.as_view(), name="signup")
    path("/accounts/login/", views.LoginView.as_view(), name="account_login"),
    path("/accounts/signup/", views.SignupView.as_view(), name="account_signup"),
    path("/accounts/logout/", views.LogoutView.as_view(), name="account_logout")
]
