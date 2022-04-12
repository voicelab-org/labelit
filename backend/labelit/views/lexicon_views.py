from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import LexiconSerializer
from labelit.models import Lexicon
from labelit.filters import LexiconFilter
from django_filters.rest_framework import DjangoFilterBackend


class LexiconViewSet(viewsets.ModelViewSet):
    queryset = Lexicon.objects.all()
    serializer_class = LexiconSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LexiconFilter
