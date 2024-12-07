from rest_framework.routers import DefaultRouter

from .views import PostView


router = DefaultRouter()
router.register(r'', PostView, basename='post')

app_name = 'post'

urlpatterns = router.urls
