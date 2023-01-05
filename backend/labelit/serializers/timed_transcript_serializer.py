from rest_framework import serializers
from labelit.models import TimedTranscript, TimedTranscriptSegment
from .timed_transcript_segment_serializer import TimedTranscriptSegmentSerializer


class TimedTranscriptSerializer(serializers.ModelSerializer):

    segments = TimedTranscriptSegmentSerializer(
        many=True,
    )

    class Meta:
        model = TimedTranscript
        fields = ["id", "segments"]

    def create(self, validated_data):
        segments = validated_data.pop("segments")
        transcript = TimedTranscript(**validated_data)
        transcript.save()
        for seg in segments:
            # seg['timed_transcript_id'] = transcript.id
            seg["timed_transcript"] = transcript
            s = TimedTranscriptSegment(**seg)
            s.save()
        return transcript

    def update(self, instance, validated_data):
        segments = validated_data.pop("segments")
        for seg in segments:
            # BEGIN HACK (can't get id of seg in validated ordered_dict)
            # s = TimedTranscriptSegment.objects.get(pk=seg['id'])
            s = TimedTranscriptSegment.objects.get(
                timed_transcript=seg["timed_transcript"], start_time=seg["start_time"]
            )
            # END HACK

            s.transcript = seg["transcript"]
            s.save()
        return instance
