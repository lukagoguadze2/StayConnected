from rest_framework.generics import (
    RetrieveAPIView, 
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    SignupSerializer, 
    UserProfileSerializer,
)

from .models import User
from comment.models import Comment


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'message': 'User registered successfully',
        }
        return response


class ProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        self.count = Comment.objects.filter(
            is_correct=True, 
            author=self.request.user.id
        ).count()
        user = User.objects.get(id=self.request.user.id)

        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['answered_questions'] = self.count
        return context
 