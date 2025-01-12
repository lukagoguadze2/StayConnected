import socket
import psutil
import django

from django.db.models import Window, OrderBy, F
from django.db.models.functions import RowNumber
from django.db import connection, DatabaseError
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView

from .serializers import (
    TagSerializer,
    CreateTagSerializer
)
from .models import Tag
from .filters import PostFilter
from .serializers import LeaderBoardSerializer
from post.models import Post
from post.swagger_docs import PostDocs
from post.serializers import PostSerializer
from authentication.models import User

from .utils import django_filter_warning

from drf_yasg.utils import swagger_auto_schema

from .swagger_docs import TagDocs, LeaderBoardDocs


class CreateTagView(CreateAPIView):
    serializer_class = CreateTagSerializer
    permission_classes = [IsAuthenticated]
    doc_class = TagDocs

    @swagger_auto_schema(
        request_body=doc_class.create_tag['request_body'],
        responses=doc_class.create_tag['responses'],
        operation_description=doc_class.create_tag['operation_description'],
        operation_summary=doc_class.create_tag['operation_summary']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GetTagsView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    doc_class = TagDocs

    @swagger_auto_schema(
        operation_description=doc_class.get_tags['operation_description'],
        operation_summary=doc_class.get_tags['operation_summary']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LeaderboardView(ListAPIView):
    serializer_class = LeaderBoardSerializer
    permission_classes = [IsAuthenticated]
    doc_class = LeaderBoardDocs

    def get_queryset(self):
        return User.objects.annotate(
            rank=Window(
                expression=RowNumber(),
                order_by=OrderBy(F('rating'), descending=True)
            )
        )

    @swagger_auto_schema(
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary,
        responses=doc_class.responses
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostsFilterView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    doc_class = PostDocs

    @django_filter_warning
    def get_queryset(self):
        return Post.objects.annotate_with_seen_by_user(
            user=self.request.user
        )

    @swagger_auto_schema(
        operation_description=doc_class.filter_post['operation_description'],
        operation_summary=doc_class.filter_post['operation_summary'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class HealthcheckAPIView(APIView):
    """
    A simple health check API that returns the status of the server and
    system information.
    """

    def get(self, request, *args, **kwargs):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        django_version = django.get_version()

        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')

        data = {
            "status": "healthy",
            "status_code": 200,
            "hostname": hostname,
            "ip_address": ip_address,
            "django_version": django_version,
            "system_metrics": {
                "cpu_usage_percent": cpu_usage,
                "memory": {
                    "total": f"{memory.total / (1024 ** 3):.2f} GB",
                    "available": f"{memory.available / (1024 ** 3):.2f} GB",
                    "used_percent": memory.percent,
                },
                "disk_usage": {
                    "total": f"{disk_usage.total / (1024 ** 3):.2f} GB",
                    "used": f"{disk_usage.used / (1024 ** 3):.2f} GB",
                    "free": f"{disk_usage.free / (1024 ** 3):.2f} GB",
                    "used_percent": disk_usage.percent,
                }
            }
        }

        return Response(data)


class DatabaseHealthcheckAPIView(APIView):
    """
    A health check API to verify database connection status and basic
    information.
    """

    def get(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
            db_status = "healthy"
            status_code = 200
        except DatabaseError:
            db_status = "unhealthy"
            status_code = 503
        
        if "sqlite" not in connection.settings_dict["ENGINE"]:
            db_info = {
                "status": db_status,
                "status_code": status_code,
                "database_engine": connection.settings_dict["ENGINE"],
                "database_name": connection.settings_dict["NAME"],
                "host": connection.settings_dict["HOST"],
                "port": connection.settings_dict["PORT"],
            }

            return Response(db_info, status=status_code)

        return Response(
            {"detail": "Current database does not support health checks."},
            status=503
        )
