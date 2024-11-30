from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostView

app_name = 'post'

router = DefaultRouter()
router.register('', PostView, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
