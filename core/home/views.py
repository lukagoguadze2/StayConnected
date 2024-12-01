import socket
import psutil
import django

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView

from .serializers import (
    CreateTagSerializer,
    TagSerializer,
)
from .models import Tag
from post.models import Post
from .filters import PostFilter
from authentication.models import User
from post.serializers import PostSerializer
from authentication.serializers import UserProfileSerializer


class CreateTagView(CreateAPIView):
    serializer_class = CreateTagSerializer
    permission_classes = [IsAuthenticated]


class GetTagsView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.all()


class LeaderboardView(ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.order_by('-rating')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ranked_users = []
        previous_rating = None
        current_rank = 0

        for index, user in enumerate(queryset, start=1):
            if user.rating != previous_rating:
                current_rank = index
                previous_rating = user.rating

            serialized_user = UserProfileSerializer(user).data
            serialized_user['rank'] = current_rank 

            ranked_users.append(serialized_user)

        return Response(ranked_users)
    

class PostsFilterView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]  
    filterset_class = PostFilter  

    def get_queryset(self):
        return Post.objects.all()
    

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
