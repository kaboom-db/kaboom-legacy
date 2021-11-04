from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as rf_views
from .obtain_tokens import CustomAuthToken

app_name = 'users'
urlpatterns = [
    path('signup/', views.CreateUser.as_view(), name='index'),
    path('login/', CustomAuthToken.as_view(), name='token')
]