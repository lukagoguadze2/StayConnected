from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentView, PostCommentsView

app_name = 'comment'

router = DefaultRouter()
router.register('', CommentView, basename='comments')

urlpatterns = [
    path('<int:post_id>/', PostCommentsView.as_view(), name='post_comments'),
    path('', include(router.urls)),
]
