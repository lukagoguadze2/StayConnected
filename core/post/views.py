from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet

from .models import Post, PostReaction
from .serializers import CreatePostSerializer, LikePostSerializer


class PostView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    queryset = Post.objects.all()

    def __react_on_post(self, request, *args, **kwargs):
        post = self.get_object()
        reaction, created = PostReaction.objects.get_or_create(
            post=post, user=request.user
        )

        if not created:
            return Response(
                {
                    "detail": f"User have already {'' if reaction.reaction_type else 'dis'}liked this post."
                },
                status=status.HTTP_409_CONFLICT)

        reaction.reaction_type = kwargs.get('reaction_type')
        reaction.save()

        return Response(status=status.HTTP_200_OK, data={'status': 'success'})

    @action(detail=False, methods=['post'], serializer_class=CreatePostSerializer, name='create_post')
    def create_post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], serializer_class=None, name='like_post')
    def like_post(self, request, *args, **kwargs):
        return self.__react_on_post(request, *args, **kwargs, reaction_type=PostReaction.LIKE)

    @action(detail=True, methods=['post'], serializer_class=None, name='dislike_post')
    def dislike_post(self, request, *args, **kwargs):
        return self.__react_on_post(request, *args, **kwargs, reaction_type=PostReaction.DISLIKE)

    @action(detail=True, methods=['delete'], serializer_class=None, name='remove_reaction')
    def remove_reaction(self, request, *args, **kwargs):
        try:
            PostReaction.objects.get(
                post=self.get_object(), user=self.request.user
            ).delete()
        except PostReaction.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': 'User have not reacted to this post yet.'}
            )

        return Response(status=status.HTTP_200_OK, data={'status': 'success'})

    @action(detail=True, methods=['put'], serializer_class=LikePostSerializer, name='like_post')
    def update_reaction(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                reaction = PostReaction.objects.get(
                    post=self.get_object(), user=self.request.user
                )
            except PostReaction.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={'detail': 'User have not reacted to this post yet.'}
                )

            if reaction.reaction_type == serializer.validated_data['reaction_type']:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'success'})

            reaction.reaction_type = serializer.validated_data['reaction_type']
            reaction.save()

            return Response(status=status.HTTP_200_OK, data={'status': 'success'})

