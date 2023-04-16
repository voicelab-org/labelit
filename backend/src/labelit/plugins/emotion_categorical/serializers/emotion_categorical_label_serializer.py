from rest_framework import serializers
from labelit.models import (
    EmotionCategoricalLabel,
)


class EmotionCategoricalLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionCategoricalLabel
        fields = [
            "id",
            "task",
            "tags_with_intensities",
        ]
