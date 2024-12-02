from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view

description = """
Welcome to the StayConnected API documentation. This API allows users to interact with the StayConnected platform, providing access to various features designed for seamless communication and data management. Below you'll find details about the available endpoints, request/response structures, and usage guidelines.

## Overview
Nothing yet.

---
## Notes
- For more details on each endpoint, including request/response structures and usage guidelines, refer to the API documentation below.
- You can also test the endpoints directly from the documentation by clicking on the "Try it out" button and providing the required parameters.
- Also, you can view the response body by clicking on the "Execute" button in 'try it out' section, to do this you need to provide the required parameters in the request body.
- For endpoints requiring the access token, make sure to include it in the `Authorization` header as `Bearer <access_token>`. You can do this by clicking on the "Authorize" button and providing the access token in the input field.
---
"""


schema_view = get_schema_view(
    openapi.Info(
        title="StayConnected API Documentation",
        default_version='v1',
        description=description,
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
