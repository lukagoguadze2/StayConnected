from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins, GenericViewSet

from .models import Post, PostReaction, PostSeen
from .serializers import (
    PostSerializer,
    LikePostSerializer,
    CreatePostSerializer
)

from home.serializers import EmptySerializer
from home.reactions import (
    react_on_entity, 
    remove_reaction, 
    update_reaction
)


class PostView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin,
               GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.annotate_with_seen_by_user(
            user=self.request.user
        ) if self.request.user.is_authenticated else None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        if self.request.method == "POST":
            return CreatePostSerializer

        return super().get_serializer_class()

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
        serializer_class=CreatePostSerializer, 
        name='create_post', 
        url_path='create'
    )
    def create_post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, 
        methods=['post'], 
        serializer_class=EmptySerializer, 
        name='like_post'
    )
    def like_post(self, request, *args, **kwargs):
        return react_on_entity(
            self,
            request, *args, **kwargs,
            model=PostReaction,
            object='post',
            reaction_type=PostReaction.LIKE
        )

    @action(
        detail=True, 
        methods=['post'], 
        serializer_class=EmptySerializer, 
        name='dislike_post'
    )
    def dislike_post(self, request, *args, **kwargs):
        return react_on_entity(
            self,
            request, *args, **kwargs,
            model=PostReaction,
            object='post',
            reaction_type=PostReaction.DISLIKE
        )

    @action(
        detail=True, 
        methods=['delete'],
        serializer_class=EmptySerializer,
        name='remove_reaction'
    )
    def remove_reaction(self, request, *args, **kwargs):
        return remove_reaction(
            self,
            request, *args, **kwargs,
            model=PostReaction,
            object='post'
        )

    @action(
        detail=True, 
        methods=['put'], 
        serializer_class=LikePostSerializer, 
        name='update_reaction'
    )
    def update_reaction(self, request, *args, **kwargs):
        return update_reaction(
            self,
            request, *args, **kwargs,
            model=PostReaction,
            object='post'
        )
