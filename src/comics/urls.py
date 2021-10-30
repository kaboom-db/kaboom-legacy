from django.urls import path
from . import views

app_name = 'comics'
urlpatterns = [
    path('', views.index, name='index'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('issues/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('publishers/<int:publisher_id>/', views.publisher_detail, name='publisher_detail'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('characters/<int:character_id>/', views.character_detail, name='character_detail'),
    path('year/<int:year>/', views.series_year, name='series_year')
]