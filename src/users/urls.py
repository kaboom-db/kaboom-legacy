from django.urls import path, include
from . import views
from .obtain_tokens import CustomAuthToken

app_name = 'users'
urlpatterns = [
    path('signup/', views.CreateUser.as_view(), name='index'),
    path('login/', CustomAuthToken.as_view(), name='token'),
    path('comics/series/', views.GetUserSubscriptions.as_view(), name='get-sub'),
    path('comics/series/add/', views.AddUserSubscription.as_view(), name='add-sub'),
    path('comics/series/rate/', views.AddUserSeriesRating.as_view(), name='rate-sub'),
    path('comics/series/remove/', views.RemoveUserSubscription.as_view(), name='remove-sub'),
    path('comics/issues/', views.GetUserReadIssues.as_view(), name='get-issues'),
    path('comics/issues/add/', views.AddUserReadIssue.as_view(), name='add-issues'),
    path('comics/issues/remove/', views.RemoveUserReadIssue.as_view(), name='remove-issues'),
    path('comics/issues/remove/clean/', views.CleanUserReadIssues.as_view(), name='clean-issues'),
]