from django.urls import path
from . import views

app_name = 'comics'
urlpatterns = [
    path('', views.index, name='index'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('issues/<int:issue_id>/', views.issue_detail, name='issue_detail')
]