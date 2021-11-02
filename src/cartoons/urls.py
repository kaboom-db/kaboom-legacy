from django.urls import path, include
from . import views
from rest_framework import routers

routerCartoons = routers.DefaultRouter()
routerCartoons.register(r'series', views.SeriesView, basename='series')

app_name = 'cartoons'
urlpatterns = [
    path('', include(routerCartoons.urls), name='index')
]