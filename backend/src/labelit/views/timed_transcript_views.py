from rest_framework import viewsets
from rest_framework import permissions
from labelit.serializers import TimedTranscriptSerializer
from labelit.models import TimedTranscript


class TimedTranscriptViewSet(viewsets.ModelViewSet):
    queryset = TimedTranscript.objects.all()
    serializer_class = TimedTranscriptSerializer
    permission_classes = [permissions.IsAuthenticated]
