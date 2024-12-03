from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError, NotFound

from home.serializers import EmptySerializer
from .models import Comment, CommentReaction
from post.serializers import LikePostSerializer
from .serializers import (
    CreateCommentSerializer,
    GetPostCommentsSerializer,
)
from .permissions import IsPostOwner
from home import ratings
from home.reactions import (
    react_on_entity, 
    remove_reaction, 
    update_reaction
)

from drf_yasg.utils import swagger_auto_schema
from .swagger_docs import CommentDocs


class CommentView(DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.prefetch_related('author')
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]
    doc_class = CommentDocs

    @swagger_auto_schema(
        operation_description=doc_class.create_comment['operation_description'],
        operation_summary=doc_class.create_comment['operation_summary']
    )
    @action(
        detail=False, 
        methods=['post'], 
        url_path='create', 
        url_name='create_comment', 
        serializer_class=CreateCommentSerializer,
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
        comment.save()
        
        author = comment.author
        author.update_rating(ratings.COMMENT_MARKED_AS_ANSWER)
        
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
        serializer_class=EmptySerializer,
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
        comment.save()
        return Response({'detail': 'Comment unmarked as correct'})

    @swagger_auto_schema(
        operation_description=doc_class.like_comment['operation_description'],
        operation_summary=doc_class.like_comment['operation_summary']
    )
    @action(
        detail=True, 
        methods=['post'], 
        serializer_class=EmptySerializer, 
        name='like_comment'
    )
    def like_comment(self, request, *args, **kwargs):
        return react_on_entity(
            request, *args, **kwargs,
            model=CommentReaction,
            object='comment',
            reaction_type=CommentReaction.LIKE
        )

    @swagger_auto_schema(
        operation_description=doc_class.dislike_comment['operation_description'],
        operation_summary=doc_class.dislike_comment['operation_summary']
    )
    @action(
        detail=True, 
        methods=['post'], 
        serializer_class=EmptySerializer, 
        name='dislike_comment'
    )
    def dislike_comment(self, request, *args, **kwargs):
        return react_on_entity(
            request, *args, **kwargs,
            model=CommentReaction,
            object='comment',
            reaction_type=CommentReaction.DISLIKE
        )

    @swagger_auto_schema(
        operation_description=doc_class.remove_reaction['operation_description'],
        operation_summary=doc_class.remove_reaction['operation_summary']
    )
    @action(
        detail=True, 
        methods=['delete'], 
        serializer_class=EmptySerializer, 
        name='remove_reaction'
    )
    def remove_reaction(self, request, *args, **kwargs):
        return remove_reaction(
            request, *args, **kwargs,
            model=CommentReaction,
            object='comment'
        )
    
    @swagger_auto_schema(
        operation_description=doc_class.update_reaction['operation_description'],
        operation_summary=doc_class.update_reaction['operation_summary']
    )
    @action(
        detail=True, 
        methods=['put'], 
        serializer_class=LikePostSerializer, 
        name='update_reaction'
    )
    def update_reaction(self, request, *args, **kwargs):
        return update_reaction(
            request, *args, **kwargs,
            model=CommentReaction,
            object='comment'
        )
        
    
    @swagger_auto_schema(
        operation_description=doc_class.delete_comment['operation_description'],
        operation_summary=doc_class.delete_comment['operation_summary']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CommentPagination(PageNumberPagination):
    page_size = 10


class PostCommentsView(ListAPIView):
    serializer_class = GetPostCommentsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination
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
            raise NotFound("Post with the given ID does not exist.")
        
        return (
            Comment.objects
            .prefetch_related('author', 'post')
            .filter(post_id=post_id)
        )
