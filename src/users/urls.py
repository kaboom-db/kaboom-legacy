from django.urls import path, include
from . import views
from . import comics_views
from .obtain_tokens import CustomAuthToken

app_name = 'users'
urlpatterns = [
    path('signup/', views.CreateUser.as_view(), name='index'),
    path('login/', CustomAuthToken.as_view(), name='token'),
    path('comics/series/', comics_views.GetUserSubscriptions.as_view(), name='get-sub'),
    path('comics/series/add/', comics_views.AddUserSubscription.as_view(), name='add-sub'),
    path('comics/series/rate/', comics_views.AddUserSeriesRating.as_view(), name='rate-sub'),
    path('comics/series/remove/', comics_views.RemoveUserSubscription.as_view(), name='remove-sub'),
    path('comics/issues/', comics_views.GetUserReadIssues.as_view(), name='get-issues'),
    path('comics/issues/add/', comics_views.AddUserReadIssue.as_view(), name='add-issues'),
    path('comics/issues/remove/', comics_views.RemoveUserReadIssue.as_view(), name='remove-issues'),
    path('comics/issues/remove/clean/', comics_views.CleanUserReadIssues.as_view(), name='clean-issues'),
]