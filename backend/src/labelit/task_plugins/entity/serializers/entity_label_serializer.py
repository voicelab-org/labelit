from rest_framework import serializers
from labelit.models import (
    EntityLabel,
)


class EntityLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityLabel
        fields = [
            "id",
            "name",
            "task",
            "color",
            "start_offset",
            "end_offset",
            "source_label",
        ]
