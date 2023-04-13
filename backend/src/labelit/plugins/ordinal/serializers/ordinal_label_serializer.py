from rest_framework import serializers
from labelit.models import (
    OrdinalLabel,
)


class OrdinalLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdinalLabel
        fields = [
            "id",
            "name",
            "task",
            "color",
            "transcript",
        ]
