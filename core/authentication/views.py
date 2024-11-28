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
        return User.objects.get(id=self.request.user.id)
    