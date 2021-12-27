from django.urls import path, include
from . import views
from . import comics_views
from . import cartoons_views
from .obtain_tokens import CustomAuthToken

app_name = 'users'
urlpatterns = [
    path('signup/', views.CreateUser.as_view(), name='index'),
    path('login/', CustomAuthToken.as_view(), name='token'),
    path('<int:user_id>/follow/', views.FollowUser.as_view(), name='follow-user'),
    path('<int:user_id>/unfollow/', views.UnfollowUser.as_view(), name='unfollow-user'),
    path('thoughts/', views.GetThoughts.as_view(), name='get-thoughts'),
    path('thoughts/types/', views.GetThoughtTypes.as_view(), name='get-thought-types'),
    path('thoughts/add/', views.AddThought.as_view(), name='add-thoughts'),
    path('thoughts/<int:thought_id>/', views.GetThought.as_view(), name='get-thought'),
    path('thoughts/<int:thought_id>/remove/', views.RemoveThought.as_view(), name='remove-thoughts'),
    path('thoughts/<int:thought_id>/like/', views.LikeThought.as_view(), name='like-thoughts'),
    path('thoughts/<int:thought_id>/edit/', views.EditThought.as_view(), name='edit-thoughts'),
    path('comics/subscriptions/', comics_views.GetUserSubscriptions.as_view(), name='get-sub'),
    path('comics/subscriptions/add/', comics_views.AddUserSubscription.as_view(), name='add-sub'),
    path('comics/subscriptions/rate/', comics_views.AddUserSeriesRating.as_view(), name='rate-sub'),
    path('comics/subscriptions/remove/', comics_views.RemoveUserSubscription.as_view(), name='remove-sub'),
    path('comics/issues/', comics_views.GetUserReadIssues.as_view(), name='get-issues'),
    path('comics/issues/add/', comics_views.AddUserReadIssue.as_view(), name='add-issues'),
    path('comics/issues/remove/', comics_views.RemoveUserReadIssue.as_view(), name='remove-issues'),
    path('comics/issues/remove/clean/', comics_views.CleanUserReadIssues.as_view(), name='clean-issues'),
    path('cartoons/subscriptions/', cartoons_views.GetUserSubscriptions.as_view(), name='get-cartoons-sub'),
    path('cartoons/subscriptions/add/', cartoons_views.AddUserSubscription.as_view(), name='add-cartoons-sub'),
    path('cartoons/subscriptions/rate/', cartoons_views.AddUserSeriesRating.as_view(), name='rate-cartoons-sub'),
    path('cartoons/subscriptions/remove/', cartoons_views.RemoveUserSubscription.as_view(), name='remove-cartoons-sub'),
    path('cartoons/episodes/', cartoons_views.GetUserWatchedEpisodes.as_view(), name='get-episodes'),
    path('cartoons/episodes/add/', cartoons_views.AddUserWatchedEpisode.as_view(), name='add-episodes'),
    path('cartoons/episodes/remove/', cartoons_views.RemoveUserWatchedEpisode.as_view(), name='remove-episodes'),
    path('cartoons/episodes/remove/clean/', cartoons_views.CleanUserWatchedEpisodes.as_view(), name='clean-episodes'),
]