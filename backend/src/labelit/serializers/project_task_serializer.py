from rest_framework import serializers
from labelit.models import ProjectTask
from rest_polymorphic.serializers import PolymorphicSerializer
from .label_serializer import LabelPolymorphicSerializer


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = [
            "task",
            "project",
            "order",
        ]
