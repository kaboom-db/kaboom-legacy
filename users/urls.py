from django.urls import path
from . import views
from . import comics_views
from . import cartoons_views
from .obtain_tokens import CustomAuthToken

app_name = 'users'
urlpatterns = [
    path('signup/', views.CreateUser.as_view(), name='index'),
    path('login/', CustomAuthToken.as_view(), name='token'),
    path('upload/', views.ImageRequestView.as_view(), name='image-request'),
    path('report/', views.ReportView.as_view(), name='report'),
    path('users/', views.GetUsersView.as_view(), name='get-users'),
    path('users/<str:username>/', views.SpecificUserView.as_view(), name='user'),
    path('users/<str:username>/follow/', views.FollowUser.as_view(), name='follow-user'),
    path('users/<str:username>/followers/', views.GetUsersFollowers.as_view(), name='followers-user'),
    path('users/<str:username>/following/', views.GetUsersFollowing.as_view(), name='following-user'),
    path('users/<str:username>/unfollow/', views.UnfollowUser.as_view(), name='unfollow-user'),
    path('thoughts/', views.GetThoughts.as_view(), name='get-thoughts'),
    path('thoughts/types/', views.GetThoughtTypes.as_view(), name='get-thought-types'),
    path('thoughts/add/', views.AddThought.as_view(), name='add-thoughts'),
    path('thoughts/<int:thought_id>/', views.SpecificThoughtView.as_view(), name='specific-thought'),
    path('thoughts/<int:thought_id>/like/', views.LikeThought.as_view(), name='like-thoughts'),
    path('thoughts/<int:thought_id>/unlike/', views.UnlikeThought.as_view(), name='unlike-thoughts'),
    path('thoughts/<int:thought_id>/comments/', views.CommentView.as_view(), name='comment-thoughts'),
    path('thoughts/<int:thought_id>/comments/<int:comment_id>/', views.SpecificCommentView.as_view(), name='comment-thoughts'),
    path('comics/subscriptions/', comics_views.ComicSubscriptionsView.as_view(), name='get-sub'),
    path('comics/subscriptions/rate/', comics_views.AddUserSeriesRating.as_view(), name='rate-sub'),
    path('comics/readissues/', comics_views.UserReadIssuesView.as_view(), name='get-issues'),
    path('comics/readissues/clean/', comics_views.CleanUserReadIssues.as_view(), name='clean-issues'),
    path('cartoons/subscriptions/', cartoons_views.CartoonSubscriptionsView.as_view(), name='get-cartoons-sub'),
    path('cartoons/subscriptions/rate/', cartoons_views.AddUserSeriesRating.as_view(), name='rate-cartoons-sub'),
    path('cartoons/episodes/', cartoons_views.UserWatchedEpisodesView.as_view(), name='get-episodes'),
    path('cartoons/episodes/clean/', cartoons_views.CleanUserWatchedEpisodes.as_view(), name='clean-episodes'),
]