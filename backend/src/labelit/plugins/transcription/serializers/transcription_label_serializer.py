from rest_framework import serializers
from labelit.models import (
    TranscriptionLabel,
)


class TranscriptionLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionLabel
        fields = [
            "id",
            "name",
            "task",
            "color",
            "transcript",
        ]
