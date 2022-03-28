from rest_framework import serializers
from labelit.models import TimedTranscriptSegment


class TimedTranscriptSegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimedTranscriptSegment
        fields = [
            'id',
            'timed_transcript',
            'transcript',
            'start_time',
        ]
