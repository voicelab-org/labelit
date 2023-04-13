from rest_framework import serializers
from labelit.models import (
    RealtimeVideoDimensionalLabel,
)


class RealtimeVideoDimensionalLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeVideoDimensionalLabel
        fields = [
            "id",
            "task",
            "sequence",
            "summative",
        ]
