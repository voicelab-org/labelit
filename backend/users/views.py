
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import User
from .serializers import UserSerializer, UserListSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin




class CreateUserView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdmin, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdmin, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )

    # queryset = User.objects.all()
    queryset = User.objects.filter(is_staff=False).order_by('first_name')  # only getting non-QA users,
    # TODO: change when needed, but then add filtering

    serializer_class = UserListSerializer

    def get_serializer_class(self):
        if self.request.user.is_admin : 
            return UserSerializer
        return super().get_serializer_class()


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)