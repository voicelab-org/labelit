from rest_framework import serializers
from labelit.models import (
    TranscriptionTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class CreateOrUpdateTranscriptionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionTask
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "archived",
            "html_guidelines",
        ]


class TranscriptionTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = TranscriptionTask
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
