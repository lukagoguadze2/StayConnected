from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="StayConnected API Documentation",
        default_version='v1',
        description="API documentation for StayConnected. Use this to understand available endpoints.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
