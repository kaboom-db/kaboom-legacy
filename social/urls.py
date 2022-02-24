from django.urls import path, include
from . import views
from rest_framework import routers

routerSocial = routers.DefaultRouter()
routerSocial.register(r'thoughts', views.ThoughtView, basename='thoughts')

app_name = 'social'
urlpatterns = [
    path('', include(routerSocial.urls), name='index')
]