from rest_framework import serializers
from labelit.models import Task
from rest_polymorphic.serializers import PolymorphicSerializer
from .label_serializer import LabelPolymorphicSerializer
from labelit.services.polymorphic_serializer_mapping_creator import (
    create_polymorphic_serializer_mapping,
)


class CreateOrUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "labels",
            "archived",
        ]


create_or_update_mappping = create_polymorphic_serializer_mapping(
    is_create_or_update=True
)


class CreateOrUpdateTaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = create_or_update_mappping


class TaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "projects",
            "can_documents_be_invalidated",
            "labels",
            "html_guidelines",
            "archived",
            "created_at",
            "updated_at",
        ]


mapping = create_polymorphic_serializer_mapping()


class TaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = mapping
