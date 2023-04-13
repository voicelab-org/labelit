from rest_framework import serializers
from labelit.models import (
    RealtimeVideoDimensionalTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class CreateOrUpdateRealtimeVideoDimensionalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeVideoDimensionalTask
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "archived",
        ]


class RealtimeVideoDimensionalTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = RealtimeVideoDimensionalTask
        fields = [
            "id",
            "name",
            "projects",
            "can_documents_be_invalidated",
            "labels",
            "image",
            "html_guidelines",
            "archived",
            "created_at",
            "updated_at",
        ]
