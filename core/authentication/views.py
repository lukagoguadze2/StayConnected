from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from post.serializers import PostSerializer
from .serializers import (
    SignupSerializer,
    UserProfileSerializer
)

from .models import User
from home import ratings
from post.models import Post
from comment.models import Comment


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'detail': 'User registered successfully',
        }
        return response


class ProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['answered_questions'] = Comment.objects.filter(
                is_correct=True,
                author=self.request.user
            ).count()
        return context


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                user.update_rating(ratings.USER_LOGGED_IN)
            except User.DoesNotExist:
                pass
        return super().post(request, *args, **kwargs)


class PersonalPostView(ListAPIView):
    """View to list personal posts of the authenticated user."""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.annotate_with_seen_by_user(
            user=self.request.user
        ).filter(
            author=self.request.user
        )
