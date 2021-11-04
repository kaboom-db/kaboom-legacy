from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'users'
urlpatterns = [
    path('signup/', views.CreateUser.as_view(), name='index')
]