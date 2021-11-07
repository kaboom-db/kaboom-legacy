from django.urls import path, include
from . import views
from .obtain_tokens import CustomAuthToken

app_name = 'users'
urlpatterns = [
    path('signup/', views.CreateUser.as_view(), name='index'),
    path('login/', CustomAuthToken.as_view(), name='token'),
    path('comics/series', views.GetUserSubscriptions.as_view(), name='get-sub'),
    path('comics/series/add/', views.AddUserSubscription.as_view(), name='add-sub')#
]