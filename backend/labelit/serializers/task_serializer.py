from rest_framework import serializers
from labelit.models import (
    Task,
    CategoricalTask,
    OrdinalTask,
    TranscriptionTask,
    LiveCorrectTask,
    EntityTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from .label_serializer import LabelPolymorphicSerializer


# TODO: make this file DRYer


class TaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'html_guidelines',
            'archived',
        ]


class CategoricalTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = CategoricalTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'are_categories_exclusive',
            'labels',
            'html_guidelines',
            'archived',
        ]


class OrdinalTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = CategoricalTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'image',
            'html_guidelines',
            'archived',
        ]


class EntityTaskSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField('get_labels')

    def get_labels(self, task):
        labels = task.labels.filter(entitylabel__source_label=None)
        serializer = LabelPolymorphicSerializer(
            instance=labels,
            many=True,
            required=False,
            read_only=True
        )
        return serializer.data

    class Meta:
        model = EntityTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'image',
            'html_guidelines',
            'archived',
        ]


class TranscriptionTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = TranscriptionTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'image',
            'html_guidelines',
            'archived',
        ]


class LiveCorrectTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = LiveCorrectTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'image',
            'html_guidelines',
            'archived',
        ]


class TaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Task: TaskSerializer,
        CategoricalTask: CategoricalTaskSerializer,
        OrdinalTask: OrdinalTaskSerializer,
        TranscriptionTask: TranscriptionTaskSerializer,
        LiveCorrectTask: LiveCorrectTaskSerializer,
        EntityTask: EntityTaskSerializer,
    }
