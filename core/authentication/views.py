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


from rest_framework_simplejwt.views import TokenObtainPairView

from home import ratings


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