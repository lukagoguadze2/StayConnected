from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    GenericAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView

from rest_framework import status
from rest_framework.response import Response

from post.serializers import PostSerializer
from .serializers import (
    SignupSerializer,
    UserProfileSerializer,
    ResetPasswordSerializer,
    ResetPasswordRequestSerializer
)

from .models import User
from home import ratings
from post.models import Post
from comment.models import Comment

from drf_yasg.utils import swagger_auto_schema

from .swagger_docs import (
    LoginDocs,
    LogOutDocs,
    SignupDocs,
    ProfileDocs,
    ProfilePostsDocs,
    ResetPasswordDocs,
    ResetPasswordRequestDocs
)


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    doc_class = SignupDocs

    @swagger_auto_schema(
        request_body=doc_class.request_body,
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'detail': 'User registered successfully',
        }
        return response


class ProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    doc_class = ProfileDocs
    
    @swagger_auto_schema(
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
    doc_class = LoginDocs
    
    @swagger_auto_schema(
        request_body=doc_class.request_body,
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary,
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                user.update_rating(ratings.USER_LOGGED_IN)
            except User.DoesNotExist:
                pass
        return super().post(request, *args, **kwargs)
    

class LogOutView(TokenBlacklistView):
    doc_class = LogOutDocs
    
    @swagger_auto_schema(
        request_body=doc_class.request_body,
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary,
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = {
            'detail': 'User logged out successfully, refresh token blacklisted',
        }
        return response
    

class PersonalPostView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    doc_class = ProfilePostsDocs
    
    @swagger_auto_schema(
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.annotate_with_seen_by_user(
            user=self.request.user
        ).filter(
            author=self.request.user
        )


class ResetPasswordRequestView(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    http_method_names = ['post']
    doc_class = ResetPasswordRequestDocs
    
    @swagger_auto_schema(
        request_body=doc_class.request_body,
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {"detail": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data={"email": email})
        if serializer.is_valid():
            if User.objects.filter(email=email).exists():
                return Response(
                    {
                        "detail": "Password can be reset for this email.", 
                        "email": email
                    },
                    
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "No user found with this email."},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    http_method_names = ['put']
    doc_class = ResetPasswordDocs
    
    def get_object(self):
        return User.objects.filter(email=self.request.data.get('email')).first()
    
    @swagger_auto_schema(
        request_body=doc_class.request_body,
        responses=doc_class.responses,
        operation_description=doc_class.operation_description,
        operation_summary=doc_class.operation_summary
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Response(
                {'detail': 'You are already logged in'},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(
                {'detail': 'Password reset successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    