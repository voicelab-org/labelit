from rest_framework import serializers
from labelit.models import (
    TextEditionLabel,
)


class TextEditionLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextEditionLabel
        fields = [
            "id",
            "name",
            "task",
            "color",
            "transcript",
        ]
