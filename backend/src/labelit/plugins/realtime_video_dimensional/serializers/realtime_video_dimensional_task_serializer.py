from rest_framework import serializers
from labelit.models import (
    RealtimeVideoDimensionalTask,
)
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class CreateOrUpdateRealtimeVideoDimensionalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeVideoDimensionalTask
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "archived",
            "html_guidelines",
        ]


class RealtimeVideoDimensionalTaskSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField("get_labels")

    def get_labels(self, task):
        labels = task.labels.all()
        serializer = LabelPolymorphicSerializer(
            instance=labels, many=True, required=False, read_only=True
        )
        return serializer.data

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
