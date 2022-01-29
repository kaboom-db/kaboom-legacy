from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/', views.docs, name='docs'),
    path('tocs/', views.tocs, name='tocs')
]