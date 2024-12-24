from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index),
    path('login', auth_views.LoginView.as_view()),
    path('logout', auth_views.LogoutView.as_view())
]