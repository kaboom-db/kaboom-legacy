from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:series_id>/', views.series_detail, name='detail')
]