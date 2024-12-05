from typing import Literal
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from home.serializer_utils import SerializerFactory
from home.serializers import EmptySerializer
from post.models import PostReaction, Post
from comment.models import CommentReaction, Comment

from home import ratings
from post.permissions import HasObjectPermission
from post.serializers import LikePostSerializer

from drf_yasg.utils import swagger_auto_schema
from comment.swagger_docs import CommentDocs


def react_on_entity(self, request, *_, **kwargs):
    """
    React on the entity (post/comment) with like/dislike.
    kwargs:
        model: Reaction model
        object (str): Object type (post/comment)
        reaction_type: Reaction type (true/false)
    """
    assert getattr(self, 'get_object'), 'get_object method not found.'

    reaction_model: PostReaction | CommentReaction = kwargs.pop("model")
    object_type: Literal['post', 'comment'] = kwargs.pop("object")
    reaction_type: bool = kwargs.pop('reaction_type')
    object_model: Post | Comment = getattr(self, 'get_object')

    reaction = reaction_model.objects.filter(
        user=request.user,
        **{object_type: object_model}
    ).first()

    if reaction:
        prefix = '' if reaction.reaction_type else 'dis'
        return Response(
            {
                "detail": (
                    f"User have already {prefix}liked this {object_type}."
                )
            },
            status=status.HTTP_409_CONFLICT
        )

    reaction = reaction_model.objects.create(
        user=request.user,
        **{object_type: object_model},
        reaction_type=reaction_type
    )

    if object_type == 'post':
        if reaction_type == reaction_model.LIKE:
            object_model.author.update_rating(ratings.POST_LIKE)
        else:
            object_model.author.update_rating(ratings.POST_DISLIKE)
            request.user.update_rating(ratings.USER_DISLIKED_POST)

    elif object_type == 'comment':
        if reaction_type == reaction_model.LIKE:
            object_model.author.update_rating(ratings.COMMENT_LIKE)
        else:
            object_model.author.update_rating(ratings.COMMENT_DISLIKE)
            request.user.update_rating(ratings.USER_DISLIKED_COMMENT)
    else:
        raise ValueError('Invalid object type.')

    reaction.save()

    return Response(status=status.HTTP_200_OK, data={'detail': 'success'})


def remove_reaction(self, request, *_, **kwargs):
    """
    Remove the reaction from the entity (post/comment).

    kwargs:
        model: Reaction model
        object (str): Object type (post/comment)
    """
    assert getattr(self, 'get_object'), 'get_object method not found.'

    reaction_model: PostReaction | CommentReaction = kwargs.pop("model")
    object_type: Literal['post', 'comment'] = kwargs.pop("object")
    object_model: Post | Comment = getattr(self, 'get_object')

    try:
        reaction = reaction_model.objects.get(
            user=request.user,
            **{object_type: object_model}
        )
        if object_type == 'post':
            if reaction.reaction_type == reaction_model.LIKE:
                object_model.author.update_rating(
                    -ratings.POST_LIKE * bool(request.user.rating)
                )
            else:
                object_model.author.update_rating(
                    -ratings.POST_DISLIKE * bool(request.user.rating)
                )
                request.user.update_rating(
                    -ratings.USER_DISLIKED_POST * bool(request.user.rating)
                )

        elif object_type == 'comment':
            if reaction.reaction_type == reaction_model.LIKE:
                object_model.author.update_rating(
                    -ratings.COMMENT_LIKE * bool(request.user.rating)
                )
            else:
                object_model.author.update_rating(
                    -ratings.COMMENT_DISLIKE * bool(request.user.rating)
                )
                request.user.update_rating(
                    -ratings.USER_DISLIKED_COMMENT * bool(request.user.rating)
                )
        else:
            raise ValueError('Invalid object type.')

        reaction.delete()

    except reaction_model.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                'detail': f'User have not reacted to this {object_type} yet.'
            }
        )

    return Response(status=status.HTTP_200_OK, data={'detail': 'success'})


def update_reaction(self, request, *_, **kwargs):
    """
    Update the reaction on the entity (post/comment).

    kwargs:
        model: Reaction model
        object (str): Object type (post/comment)
    """
    assert getattr(self, 'get_object'), 'get_object method not found.'
    assert getattr(self, 'get_serializer'), 'get_serializer method not found.'

    reaction_model: PostReaction | CommentReaction = kwargs.pop("model")
    object_type: Literal['post', 'comment'] = kwargs.pop("object")
    object_model: Post | Comment = getattr(self, 'get_object')
    serializer = getattr(self, 'get_serializer')(data=request.data)

    if serializer.is_valid(raise_exception=True):
        try:
            reaction = reaction_model.objects.get(
                user=self.request.user,
                **{object_type: object_model}
            )
        except reaction_model.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'detail': (
                        f'User have not reacted to this {object_type} yet.'
                    )
                }
            )

        rt = serializer.validated_data['reaction_type']
        if reaction.reaction_type == rt:
            return Response(
                status=status.HTTP_200_OK, 
                data={'detail': 'success'}
            )

        reaction.reaction_type = serializer.validated_data['reaction_type']

        if object_type == 'post':
            if rt == reaction_model.LIKE:
                object_model.author.update_rating(
                    ratings.POST_LIKE +
                    abs(ratings.POST_DISLIKE) * bool(request.user.rating)
                )
                request.user.update_rating(
                    abs(ratings.USER_DISLIKED_POST) * bool(request.user.rating)
                )
            else:
                object_model.author.update_rating(
                    ratings.POST_DISLIKE - ratings.POST_LIKE
                )
                request.user.update_rating(ratings.USER_DISLIKED_POST)

        elif object_type == 'comment':
            if rt == reaction_model.LIKE:
                object_model.author.update_rating(
                    ratings.COMMENT_LIKE +
                    abs(ratings.COMMENT_DISLIKE) * bool(request.user.rating)
                )
                request.user.update_rating(
                    abs(ratings.USER_DISLIKED_COMMENT) * bool(request.user.rating)
                )
            else:
                object_model.author.update_rating(
                    ratings.COMMENT_DISLIKE - ratings.COMMENT_LIKE
                )
                request.user.update_rating(ratings.USER_DISLIKED_COMMENT)

        reaction.save()

        return Response(status=status.HTTP_200_OK, data={'detail': 'success'})


class ReactionModelMixin:
    __serializer_per_action = dict(
        like=EmptySerializer,
        dislike=EmptySerializer,
        update_reaction=LikePostSerializer
    )

    serializer_class = None
    reaction_model: PostReaction | CommentReaction = None
    object_type: Literal['post', 'comment'] = None

    doc_class = CommentDocs

    def get_serializer_class(self):
        if self.serializer_class is None:
            return SerializerFactory(
                EmptySerializer,
                **self.__serializer_per_action
            ).serializer_getter

        elif isinstance(self.serializer_class, SerializerFactory):
            return SerializerFactory(
                self.serializer_class.serializer_getter.default,
                **{
                    **self.serializer_class.serializer_getter.serializer_per_action,
                    **self.__serializer_per_action
                }
            ).serializer_getter

        return self.serializer_class

    @swagger_auto_schema(
        operation_description=doc_class.like['operation_description'],
        operation_summary=doc_class.like['operation_summary']
    )
    @action(
        detail=True,
        methods=['post'],
        name='like'
    )
    def like(self, request, *args, **kwargs):
        return react_on_entity(
            self,
            request, *args, **kwargs,
            model=self.reaction_model,
            object=self.object_type,
            reaction_type=self.reaction_model.LIKE
        )

    @swagger_auto_schema(
        operation_description=doc_class.dislike['operation_description'],
        operation_summary=doc_class.dislike['operation_summary']
    )
    @action(
        detail=True,
        methods=['post'],
        name='dislike'
    )
    def dislike(self, request, *args, **kwargs):
        return react_on_entity(
            self,
            request, *args, **kwargs,
            model=self.reaction_model,
            object=self.object_type,
            reaction_type=self.reaction_model.DISLIKE
        )

    @swagger_auto_schema(
        operation_description=doc_class.remove_reaction['operation_description'],
        operation_summary=doc_class.remove_reaction['operation_summary']
    )
    @action(
        detail=True,
        methods=['delete'],
        name='remove_reaction',
        permission_classes=[
            IsAuthenticated,
            HasObjectPermission,
        ],

    )
    def remove_reaction(self, request, *args, **kwargs):
        return remove_reaction(
            self,
            request, *args, **kwargs,
            model=self.reaction_model,
            object=self.object_type
        )

    @swagger_auto_schema(
        operation_description=doc_class.update_reaction['operation_description'],
        operation_summary=doc_class.update_reaction['operation_summary']
    )
    @action(
        detail=True,
        methods=['put'],
        name='update_reaction',
        permission_classes=[
            IsAuthenticated,
            HasObjectPermission,
        ],
    )
    def update_reaction(self, request, *args, **kwargs):
        return update_reaction(
            self,
            request, *args, **kwargs,
            model=self.reaction_model,
            object=self.object_type
        )
