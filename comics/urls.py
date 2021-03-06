from django.urls import path, include
from . import views
from cartoons.views import CharacterView
from rest_framework import routers

routerComics = routers.DefaultRouter()
routerComics.register(r'publishers', views.PublisherView, basename='publishers')
routerComics.register(r'characters', CharacterView, basename='characters')
routerComics.register(r'staff', views.StaffView, basename='staff')
routerComics.register(r'issues', views.IssueView, basename='issues')
routerComics.register(r'series', views.SeriesView, basename='series')
routerComics.register(r'staffpositions', views.StaffPositionsView, basename='staff-positions')
routerComics.register(r'formats', views.FormatsView, basename='formats')

app_name = 'comics'
urlpatterns = [
    path('', include(routerComics.urls), name='index')
]