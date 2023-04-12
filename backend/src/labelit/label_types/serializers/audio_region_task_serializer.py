from rest_framework import serializers
from labelit.models import (
    AudioRegionTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class CreateOrUpdateAudioRegionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRegionTask
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "color",
            "archived",
        ]


class AudioRegionTaskSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField("get_labels")

    def get_labels(self, task):
        labels = task.labels.all()
        serializer = LabelPolymorphicSerializer(
            instance=labels, many=True, required=False, read_only=True
        )
        return serializer.data

    class Meta:
        model = AudioRegionTask
        fields = [
            "id",
            "name",
            "projects",
            "can_documents_be_invalidated",
            "labels",
            "image",
            "html_guidelines",
            "archived",
            "color",
            "created_at",
            "updated_at",
        ]
