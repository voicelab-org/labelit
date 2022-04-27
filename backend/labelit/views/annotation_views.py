from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination
from labelit.serializers import AnnotationSerializer
from labelit.models import Annotation


class AnnotationPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]
