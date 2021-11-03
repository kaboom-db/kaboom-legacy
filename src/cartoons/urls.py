from django.urls import path, include
from . import views
from rest_framework import routers

routerCartoons = routers.DefaultRouter()
routerCartoons.register(r'series', views.SeriesView, basename='series')
routerCartoons.register(r'characters', views.CharacterView, basename='characters')

app_name = 'cartoons'
urlpatterns = [
    path('', include(routerCartoons.urls), name='index')
]