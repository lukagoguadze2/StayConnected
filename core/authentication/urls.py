from django.urls import include, path

from authentication.views import (
    LoginView,
    SignupView,
    LogOutView,
    ProfileView,
    PersonalPostView,
    ResetPasswordView,
    ResetPasswordRequestView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'auth'

urlpatterns = [
    path('auth/', include(
            [
                path('signup/', SignupView.as_view(), name='signup'),
                path('login/', LoginView.as_view(), name='login'),
                path('logout/', LogOutView.as_view(), name='logout'),
                path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
                path('reset-password-request/', ResetPasswordRequestView.as_view(), name='reset-password-request'),
            ]
        )
    ),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/posts/', PersonalPostView.as_view(), name='profile-posts'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
