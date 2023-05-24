from rest_framework import serializers
from labelit.models import (
    LiveCorrectLabel,
)


class LiveCorrectLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveCorrectLabel
        fields = [
            "id",
            "name",
            "task",
            "color",
            "timed_transcript",
        ]
