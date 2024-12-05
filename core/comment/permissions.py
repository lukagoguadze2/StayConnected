# permissions.py
from rest_framework.permissions import BasePermission


class IsPostOwner(BasePermission):
    """
    Custom permission to allow only the owner of the post to perform
    the action.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the post.
        """
        return obj.post.author == request.user


class IsCommentOwner(BasePermission):
    """
    Custom permission to allow only the owner of the comment to perform
    the action.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the comment.
        """
        return obj.author == request.user


class CanDeleteComment(BasePermission):
    """
    Custom permission to allow only the owner of the comment or the owner
    of the post to delete the comment.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the comment or the owner of the post.
        """
        return (
                obj.author == request.user
                or obj.post.author == request.user
                or request.user.is_staff
        )
