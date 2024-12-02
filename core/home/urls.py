from django.urls import path
from .views import (
    CreateTagView,
    GetTagsView,
    LeaderboardView,
    PostsFilterView,
    HealthcheckAPIView,
    DatabaseHealthcheckAPIView
)

app_name = 'home'

urlpatterns = [
    path('tags/create/', CreateTagView.as_view(), name='create_tag'),
    path('tags/', GetTagsView.as_view(), name='get_tags'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('posts/filter/', PostsFilterView.as_view(), name='posts-filter'),
    path('check/health/', HealthcheckAPIView.as_view(), name='healthcheck'),
    path('check/db-connection/', DatabaseHealthcheckAPIView.as_view(), name='db_connection'),
]
