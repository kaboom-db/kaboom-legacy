from django.urls import path, include
from . import views
from rest_framework import routers

routerCartoons = routers.DefaultRouter()
routerCartoons.register(r'cartoons', views.CartoonView, basename='cartoons')

app_name = 'cartoons'
urlpatterns = [
    path('', include(routerCartoons.urls), name='index')
]