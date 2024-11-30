from django.urls import path
from .views import (
    CreatePostView, 
    CreateTagView,
    GetTagsView,
    LeaderboardView,
)

app_name = 'home'

urlpatterns = [
    path('posts/create', CreatePostView.as_view(), name='create_post'),
    path('tags/create', CreateTagView.as_view(), name='create_tag'),
    path('tags/', GetTagsView.as_view(), name='get_tags'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]