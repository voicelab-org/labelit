from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import AnnotationSerializer
from labelit.models import Annotation


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]
