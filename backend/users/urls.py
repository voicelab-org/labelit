from django.urls import path, include
from rest_framework import routers
from .views import CreateUserView, UserListView, UserDetailView, Me


urlpatterns = [
    path("users/<int:pk>/", UserDetailView.as_view(), name="users_detail_view"),
    path("users/<int:pk>/", CreateUserView.as_view(), name="create_user_view"),
    path("users/", UserListView.as_view(), name="users_list_view"),
    path("users/me/", Me.as_view(), name="me"),
]
