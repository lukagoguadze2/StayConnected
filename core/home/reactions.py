from rest_framework import status
from rest_framework.response import Response

from home import ratings


def react_on_entity(self, request, *_, **kwargs):
    """
    React on the entity (post/comment) with like/dislike.
    kwargs:
        model: Reaction model
        object (str): Object type (post/comment)
        reaction_type: Reaction type (true/false)
    """
    reaction_model = kwargs.pop("model")
    object_type = kwargs.pop("object")
    reaction_type = kwargs.pop('reaction_type')
    object_model = self.get_object()

    reaction, created = reaction_model.objects.get_or_create(
        user=request.user,
        **{object_type: object_model}
    )

    if not created:
        return Response(
            {
                "detail": f"User have already {'' if reaction.reaction_type else 'dis'}liked this {object_type}."
            },
            status=status.HTTP_409_CONFLICT)

    reaction.reaction_type = reaction_type

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
    reaction_model = kwargs.pop("model")
    object_type = kwargs.pop("object")
    object_model = self.get_object()
    try:
        reaction = reaction_model.objects.get(
            user=request.user,
            **{object_type: object_model}
        )
        if object_type == 'post':
            if reaction.reaction_type == reaction_model.LIKE:
                object_model.author.update_rating(-ratings.POST_LIKE * bool(request.user.rating))
            else:
                object_model.author.update_rating(-ratings.POST_DISLIKE * bool(request.user.rating))
                request.user.update_rating(-ratings.USER_DISLIKED_POST * bool(request.user.rating))

        elif object_type == 'comment':
            if reaction.reaction_type == reaction_model.LIKE:
                object_model.author.update_rating(-ratings.COMMENT_LIKE * bool(request.user.rating))
            else:
                object_model.author.update_rating(-ratings.COMMENT_DISLIKE * bool(request.user.rating))
                request.user.update_rating(-ratings.USER_DISLIKED_COMMENT * bool(request.user.rating))
        else:
            raise ValueError('Invalid object type.')

        reaction.delete()

    except reaction_model.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={'detail': f'User have not reacted to this {object_type} yet.'}
        )

    return Response(status=status.HTTP_200_OK, data={'detail': 'success'})


def update_reaction(self, request, *_, **kwargs):
    """
    Update the reaction on the entity (post/comment).

    kwargs:
        model: Reaction model
        object (str): Object type (post/comment)
    """
    reaction_model = kwargs.pop("model")
    object_type = kwargs.pop("object")
    object_model = self.get_object()
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        try:
            reaction = reaction_model.objects.get(
                user=self.request.user,
                **{object_type: object_model}
            )
        except reaction_model.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': f'User have not reacted to this {object_type} yet.'}
            )

        rt = serializer.validated_data['reaction_type']
        if reaction.reaction_type == rt:
            return Response(status=status.HTTP_200_OK, data={'detail': 'success'})

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
                object_model.author.update_rating(ratings.POST_DISLIKE - ratings.POST_LIKE)
                request.user.update_rating(ratings.USER_DISLIKED_POST)

        elif object_type == 'comment':
            if rt == reaction_model.LIKE:
                object_model.author.update_rating(
                    ratings.COMMENT_LIKE +
                    abs(ratings.COMMENT_DISLIKE) * bool(request.user.rating)
                )
                request.user.update_rating(abs(ratings.USER_DISLIKED_COMMENT) * bool(request.user.rating))
            else:
                object_model.author.update_rating(ratings.COMMENT_DISLIKE - ratings.COMMENT_LIKE)
                request.user.update_rating(ratings.USER_DISLIKED_COMMENT)

        reaction.save()

        return Response(status=status.HTTP_200_OK, data={'detail': 'success'})
