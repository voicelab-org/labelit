from rest_framework import serializers
from labelit.models import Label
from rest_polymorphic.serializers import PolymorphicSerializer
from labelit.services.polymorphic_serializer_mapping_creator import (
    create_polymorphic_serializer_mapping,
)


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "task", "color"]


mapping = create_polymorphic_serializer_mapping(
    is_task_mapping=False,
)


mapping.update(
    {
        Label: LabelSerializer,
    }
)


class LabelPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = mapping


class LabelPolymorphicReadSerializer(PolymorphicSerializer):
    model_serializer_mapping = mapping
