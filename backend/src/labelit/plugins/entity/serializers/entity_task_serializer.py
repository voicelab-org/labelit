from rest_framework import serializers
from labelit.models import (
    EntityTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class CreateOrUpdateEntityTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityTask
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "labels",
            "archived",
            "html_guidelines",
        ]


class EntityTaskSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField("get_labels")

    def get_labels(self, task):
        labels = task.labels.filter(entitylabel__source_label=None)
        serializer = LabelPolymorphicSerializer(
            instance=labels, many=True, required=False, read_only=True
        )
        return serializer.data

    class Meta:
        model = EntityTask
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
