from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('v1/', views.v1, name='v1'),
    path('docs/', views.docs, name='docs'),
    path('tocs/', views.tocs, name='tocs'),
    path('privacy/', views.privacy, name='privacy'),
    path('profile/', views.profile, name='profile'),
    path('watched/<str:username>/', views.watched, name='watched'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dev-guides/', views.dev_guides, name='dev-guides')
]