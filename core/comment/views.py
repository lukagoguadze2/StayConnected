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
from post.serializers import LikePostSerializer
from .serializers import (
    CreateCommentSerializer,
    GetPostCommentsSerializer,
)
from .permissions import IsPostOwner
from home.reactions import ReactionModelMixin
from home import ratings


class CommentView(DestroyModelMixin,
                  ReactionModelMixin,
                  GenericViewSet):
    queryset = Comment.objects.prefetch_related('author')
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerFactory(
        CreateCommentSerializer,
        mark_correct=EmptySerializer,
        unmark_correct=EmptySerializer
    )

    # ReactionViewMixin
    reaction_model = CommentReaction
    object_type = 'comment'

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
        comment.save()
        return Response({'detail': 'Comment unmarked as correct'})


class CommentPagination(PageNumberPagination):
    page_size = 10


class PostCommentsView(ListAPIView):
    serializer_class = GetPostCommentsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if not post_id or not Comment.objects.filter(post_id=post_id).exists():
            raise NotFound("Post with the given ID does not exist.")
        
        return (
            Comment.objects
            .prefetch_related('author', 'post')
            .filter(post_id=post_id)
        )
