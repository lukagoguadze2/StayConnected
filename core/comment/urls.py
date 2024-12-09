from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentView, PostCommentsView


router = DefaultRouter()
router.register('', CommentView, basename='comment')

app_name = 'comment'

urlpatterns = [
    path('post/<int:post_id>/', PostCommentsView.as_view(), name='post_comments'),
    path('', include(router.urls)),
]
