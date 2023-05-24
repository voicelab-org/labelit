from rest_framework import serializers
from labelit.models import (
    OrdinalLabel,
)

from django.core.exceptions import ObjectDoesNotExist


class OrdinalLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdinalLabel
        fields = [
            "id",
            "name",
            "task",
            "color",
            "index",
        ]

    def create(self, validated_data):
        try:
            OrdinalLabel.objects.get(
                task=validated_data.get("task"), index=validated_data.get("index")
            )
            raise serializers.ValidationError(
                "Validation error: duplicate. A label with matching (task, index) already exists"
            )
        except ObjectDoesNotExist:
            pattern = OrdinalLabel(**validated_data)
            pattern.save()
        return pattern
