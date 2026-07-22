from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from . import views

urlpatterns = [
   path("login/",views.LoginView.as_view()),
   path("signup/",views.SignupView.as_view()),
   path("login-template/", views.login_view, name="login"),
   path("signup-template/", views.signup_view, name="signup"),
   path("logout/", views.logout_view, name="logout"),
   path("profile/", views.profile_view, name="profile"),
   path("password-change/", views.password_change_view, name="password-change"),
]
