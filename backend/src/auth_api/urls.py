from django.urls import path
from .views import (
    RegisterView,
    ChangePasswordView,
    UpdateProfileView,
    LogoutView,
    LogoutAllView,
    CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path(
        "auth/change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    path(
        "auth/update_profile/<int:pk>/",
        UpdateProfileView.as_view(),
        name="auth_update_profile",
    ),
    path("auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("auth/logout_all/", LogoutAllView.as_view(), name="auth_logout_all"),
]
