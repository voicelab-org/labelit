from rest_framework import serializers
from labelit.models import (
    OrdinalTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class CreateOrUpdateOrdinalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdinalTask
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "labels",
            "archived",
        ]


class OrdinalTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = OrdinalTask
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

