from rest_framework import serializers
from labelit.models import (
    CategoricalTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.serializers.label_serializer import LabelPolymorphicSerializer


class CategoricalTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = CategoricalTask
        fields = [
            "id",
            "name",
            "projects",
            "can_documents_be_invalidated",
            "are_categories_exclusive",
            "labels",
            "html_guidelines",
            "archived",
            "created_at",
            "updated_at",
        ]


class CreateOrUpdateCategoricalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoricalTask
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "labels",
            "archived",
        ]
