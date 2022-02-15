from django.urls import path, include
from . import views
from rest_framework import routers

routerCartoons = routers.DefaultRouter()
routerCartoons.register(r'series', views.SeriesView, basename='series')
routerCartoons.register(r'characters', views.CharacterView, basename='characters')
routerCartoons.register(r'episodes', views.EpisodeView, basename='episodes')
routerCartoons.register(r'genres', views.GenreView, basename='genres')
routerCartoons.register(r'networks', views.NetworkView, basename='networks')
routerCartoons.register(r'actors', views.VoiceActorView, basename='actors')
routerCartoons.register(r'teams', views.TeamView, basename='team')
routerCartoons.register(r'locations', views.LocationView, basename='locations')

app_name = 'cartoons'
urlpatterns = [
    path('', include(routerCartoons.urls), name='index')
]