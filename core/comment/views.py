from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError, NotFound

from home.serializer_utils import SerializerFactory
from home.serializers import EmptySerializer
from .models import Comment, CommentReaction
from .serializers import (
    CreateCommentSerializer,
    GetPostCommentsSerializer,
)
from .permissions import IsPostOwner, CanDeleteComment
from home.reactions import ReactionModelMixin
from home import ratings

from drf_yasg.utils import swagger_auto_schema
from .swagger_docs import CommentDocs


class CommentView(DestroyModelMixin,
                  ReactionModelMixin,
                  GenericViewSet):
    queryset = Comment.objects.prefetch_related('author', 'post')
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerFactory(
        CreateCommentSerializer,
        mark_correct=EmptySerializer,
        unmark_correct=EmptySerializer
    )

    doc_class = CommentDocs

    # ReactionViewMixin
    reaction_model = CommentReaction
    object_type = 'comment'

    @swagger_auto_schema(
        operation_description=doc_class.create_comment['operation_description'],
        operation_summary=doc_class.create_comment['operation_summary']
    )
    @action(
        detail=False, 
        methods=['post'], 
        url_path='create', 
        url_name='create',
    )
    def create_comment(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, 
            context={
                'author': request.user
            }
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_description=doc_class.mark_correct['operation_description'],
        operation_summary=doc_class.mark_correct['operation_summary']
    )
    @action(
        detail=True, 
        methods=['put'], 
        url_path='mark_correct', 
        url_name='mark_correct', 
        permission_classes=[
            IsAuthenticated, 
            IsPostOwner,
        ],
        serializer_class=EmptySerializer,
    )
    def mark_correct(self, request, *args, **kwargs):
        comment = self.get_object()
        
        if Comment.objects.filter(post=comment.post, is_correct=True).exists():
            raise ValidationError(
                {'detail': 'This post already has a correct answer.'}
            )
        
        comment.is_correct = True
        comment.author.update_rating(ratings.COMMENT_MARKED_AS_ANSWER)
        
        post_author = comment.post.author
        post_author.update_rating(ratings.COMMENT_AUTHOR_MARKED_AS_ANSWER)
        
        return Response({'detail': 'Comment marked as correct'})

    @swagger_auto_schema(
        operation_description=doc_class.unmark_correct['operation_description'],
        operation_summary=doc_class.unmark_correct['operation_summary']
    )
    @action(
        detail=True, 
        methods=['put'], 
        url_path='unmark_correct', 
        url_name='unmark_correct', 
        permission_classes=[
            IsAuthenticated, 
            IsPostOwner,
        ],
    )
    def unmark_correct(self, request, *args, **kwargs):
        comment = self.get_object()    
        
        if not Comment.objects.filter(post=comment.post, is_correct=True).exists():
            raise ValidationError(
                {'detail': 'This post is not marked as correct yet.'}
            )
        if not comment.is_correct:
            raise ValidationError(
                {'detail': 'This comment is not marked as correct.'}
            )

        comment.is_correct = False
        comment.author.update_rating(-ratings.COMMENT_MARKED_AS_ANSWER)

        post_author = comment.post.author
        post_author.update_rating(-ratings.COMMENT_AUTHOR_MARKED_AS_ANSWER)

        return Response({'detail': 'Comment unmarked as correct'})

    @swagger_auto_schema(
        operation_description=doc_class.delete_comment['operation_description'],
        operation_summary=doc_class.delete_comment['operation_summary']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'destroy':
            return super().get_permissions() + [CanDeleteComment()]

        return super().get_permissions()


class CommentPagination(PageNumberPagination):
    page_size = 10


class PostCommentsView(ListAPIView):
    serializer_class = GetPostCommentsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination
    filter_backends = []

    doc_class = CommentDocs

    @swagger_auto_schema(
        operation_description=doc_class.post_comments['operation_description'],
        operation_summary=doc_class.post_comments['operation_summary']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if not post_id or not Comment.objects.filter(post_id=post_id).exists():
            raise NotFound("Post with the given ID does not exist, or it has no comments.")
        
        return (
            Comment.objects
            .prefetch_related('author', 'post')
            .filter(post_id=post_id)
        )
