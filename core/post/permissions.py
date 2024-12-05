from rest_framework.permissions import BasePermission


class HasObjectPermission(BasePermission):
    """
    Custom permission to allow only the owner of the comment or the owner
    of the post to delete the comment.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the comment or the owner of the post.
        """
        return (
                getattr(obj, 'author', getattr(obj, 'user', None)) == request.user
                or request.user.is_staff
        )
