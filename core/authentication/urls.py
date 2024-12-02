from django.urls import include, path
from authentication.views import (
    SignupView,
    PersonalPostView,
    ProfileView,
    LoginView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView
)

app_name = 'auth'

urlpatterns = [
    path('auth/', include(
            [
                path('signup/', SignupView.as_view(), name='signup'),
                path('login/', LoginView.as_view(), name='login'),
                path('logout/', TokenBlacklistView.as_view(), name='logout'),
            ]
        )
    ),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/posts/', PersonalPostView.as_view(), name='profile-posts'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
