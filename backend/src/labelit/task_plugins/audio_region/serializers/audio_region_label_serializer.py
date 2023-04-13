from rest_framework import serializers
from labelit.models import (
    TranscriptionLabel,
)


class AudioRegionLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRegionLabel
        fields = [
            "id",
            "name",
            "task",
            "start",
            "end",
        ]
