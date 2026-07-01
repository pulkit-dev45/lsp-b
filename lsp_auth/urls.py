from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from . import views
urlpatterns = [
   path("login/",views.LoginView.as_view()),
   path("signup/",views.SignupView.as_view())
]