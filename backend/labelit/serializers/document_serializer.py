from rest_framework import serializers
from labelit.models import Document
from .document_sequence_serializer import DocumentSequenceSerializer
from .timed_transcript_serializer import TimedTranscriptSerializer


class DocumentSerializer(serializers.ModelSerializer):
    document_sequence = DocumentSequenceSerializer(
        read_only=True,
    )
    timed_transcript = TimedTranscriptSerializer(
        read_only=True,
    )

    class Meta:
        model = Document
        fields = [
            'id',
            'text',
            'audio_filename',
            'dataset',
            'document_sequence',
            'sequence_index',
            'timed_transcript',
        ]
