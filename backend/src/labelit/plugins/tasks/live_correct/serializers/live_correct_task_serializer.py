from rest_framework import serializers
from labelit.models import (
    LiveCorrectTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class LiveCorrectTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = LiveCorrectTask
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
