from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import DocumentSequenceSerializer
from labelit.models import DocumentSequence


class DocumentSequenceViewSet(viewsets.ModelViewSet):
    queryset = DocumentSequence.objects.all()
    serializer_class = DocumentSequenceSerializer
    permission_classes = [permissions.IsAuthenticated]
