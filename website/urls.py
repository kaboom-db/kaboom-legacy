from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/', views.docs, name='docs'),
    path('tocs/', views.tocs, name='tocs'),
    path('privacy/', views.privacy, name='privacy'),
    path('dev-guides/', views.dev_guides, name='dev-guides')
]