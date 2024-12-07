from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins, GenericViewSet

from home.serializer_utils import SerializerFactory
from .models import Post, PostReaction, PostSeen
from .permissions import HasObjectPermission
from .serializers import (
    PostSerializer,
    CreatePostSerializer
)

from home.reactions import ReactionModelMixin

from .swagger_docs import PostDocs
from drf_yasg.utils import swagger_auto_schema


class PostView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin,
               ReactionModelMixin,
               GenericViewSet):
    http_method_names = ['get', 'post', 'delete', 'put']
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerFactory(
        default=PostSerializer,
        create_post=CreatePostSerializer,
        update=CreatePostSerializer
    )

    doc_class = PostDocs

    # ReactionModelMixin
    reaction_model = PostReaction
    object_type = 'post'
    like_post_url_name = 'like_post'
    dislike_post_url_name = 'dislike_post'

    def get_queryset(self):
        return Post.objects.annotate_with_seen_by_user(
            user=self.request.user
        ) if self.request.user.is_authenticated else None

    @swagger_auto_schema(
        operation_description=doc_class.single_post['operation_description'],
        operation_summary=doc_class.single_post['operation_summary'],
        responses=doc_class.single_post['responses']
    )
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

    @swagger_auto_schema(
        operation_description=doc_class.create_post['operation_description'],
        operation_summary=doc_class.create_post['operation_summary'],
        request_body=doc_class.create_post['request_body'],
    )
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

    @swagger_auto_schema(
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=doc_class.update_post['operation_description'],
        operation_summary=doc_class.update_post['operation_summary'],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=doc_class.delete_post['operation_description'],
        operation_summary=doc_class.delete_post['operation_summary'],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'destroy':
            return super().get_permissions() + [HasObjectPermission()]

        return super().get_permissions()

