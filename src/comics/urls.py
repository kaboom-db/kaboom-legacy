from django.urls import path, include
from . import views
from rest_framework import routers

routerComics = routers.DefaultRouter()
routerComics.register(r'publishers', views.PublisherView, basename='publishers')
routerComics.register(r'characters', views.CharacterView, basename='characters')

app_name = 'comics'
urlpatterns = [
    path('api/comics/', include(routerComics.urls), name='index')
]