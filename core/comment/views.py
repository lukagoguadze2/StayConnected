from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


from .models import Comment
from .serializers import (
    CreateCommentSerializer,
    GetPostCommentsSerializer,
)
from .permissions import IsPostOwner


class CommentView(GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]
    
    @action(
        detail=False, 
        methods=['post'], 
        url_path='create', 
        url_name='create_comment', 
        serializer_class=CreateCommentSerializer,
    )
    def create_comment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'author': request.user})
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
        serializer_class=None,
    )
    def mark_correct(self, request, *args, **kwargs):
        comment = self.get_object()
        
        if Comment.objects.filter(post=comment.post, is_correct=True).exists():
            raise ValidationError({'detail': 'This post already has a correct answer.'})
        
        comment.is_correct = True
        comment.save()
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
        serializer_class=None,
    )
    def unmark_correct(self, request, *args, **kwargs):
        comment = self.get_object()    
        
        if Comment.objects.filter(post=comment.post, is_correct=False).exists():
            raise ValidationError({'detail': 'This post is not marked as correct yet.'})
            
        comment.is_correct = False
        comment.save()
        return Response({'detail': 'Comment unmarked as correct'})
    

class PostCommentsView(ListAPIView):
    serializer_class = GetPostCommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id'] 
        return Comment.objects.filter(post_id=post_id)
    