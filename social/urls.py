from django.urls import path, include
from . import views
from rest_framework import routers

routerSocial = routers.DefaultRouter()
routerSocial.register(r'thoughts', views.ThoughtView, basename='thoughts')

app_name = 'social'
urlpatterns = [
    path('', include(routerSocial.urls), name='index'),
    path('thoughts/<int:thought_id>/comments/', views.CommentView.as_view(), name='comments'),
    path('comments/<int:comment_id>/', views.SpecificCommentView.as_view(), name='spec-comments'),
    path('feed/', views.FeedView.as_view(), name='feed')
]