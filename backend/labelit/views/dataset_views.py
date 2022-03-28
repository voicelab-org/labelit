from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import DatasetSerializer
from labelit.models import Dataset


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
