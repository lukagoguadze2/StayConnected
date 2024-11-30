from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    CreateTagSerializer,
    TagSerializer,
)

from authentication.serializers import UserProfileSerializer
from post.serializers import PostSerializer

from .filters import PostFilter

from .models import Tag
from authentication.models import User
from post.models import Post
from rest_framework.response import Response


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
        
        
