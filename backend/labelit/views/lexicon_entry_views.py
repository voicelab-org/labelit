from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import LexiconEntrySerializer
from labelit.models import LexiconEntry


class LexiconEntryViewSet(viewsets.ModelViewSet):
    queryset = LexiconEntry.objects.all()
    serializer_class = LexiconEntrySerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
