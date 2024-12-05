from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins, GenericViewSet

from home.serializer_utils import SerializerFactory
from .models import Post, PostReaction, PostSeen
from .serializers import (
    PostSerializer,
    CreatePostSerializer
)

from home.reactions import ReactionModelMixin


class PostView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin,
               ReactionModelMixin,
               GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerFactory(
        PostSerializer,
        create=CreatePostSerializer,
    )

    # ReactionModelMixin
    reaction_model = PostReaction
    object_type = 'post'
    like_post_url_name = 'like_post'
    dislike_post_url_name = 'dislike_post'

    def get_queryset(self):
        return Post.objects.annotate_with_seen_by_user(
            user=self.request.user
        ) if self.request.user.is_authenticated else None

    def retrieve(self, request, *args, **kwargs):
        PostSeen.objects.get_or_create(
            post=self.get_object(), 
            user=request.user
        )
        instance = get_object_or_404(
            Post.objects.annotate_with_seen_by_user(user=self.request.user), 
            pk=self.kwargs['pk']
        )
        instance.seen_by_user = True
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False, 
        methods=['post'], 
        name='create',
        url_path='create'
    )
    def create_post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
