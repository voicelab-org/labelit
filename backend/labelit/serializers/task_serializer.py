from rest_framework import serializers
from labelit.models import (
    Task,
    CategoricalTask,
    OrdinalTask,
    TranscriptionTask,
    LiveCorrectTask,
    EntityTask,
    TextEditionTask,
    NestedCategoricalTask,
    AudioRegionTask,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from .label_serializer import LabelPolymorphicSerializer

# TODO: DRY the code


class CreateOrUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'can_documents_be_invalidated',
            'labels',
            'archived',
        ]


class CreateOrUpdateCategoricalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoricalTask
        fields = [
            'id',
            'name',
            'can_documents_be_invalidated',
            'labels',
            'archived',
        ]


class CreateOrUpdateAudioRegionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRegionTask
        fields = [
            'id',
            'name',
            'can_documents_be_invalidated',
            'color',
            'archived',
        ]


class CreateOrUpdateTextEditionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextEditionTask
        fields = [
            'id',
            'name',
            'can_documents_be_invalidated',
            'archived',
        ]


class CreateOrUpdateTranscriptionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionTask
        fields = [
            'id',
            'name',
            'can_documents_be_invalidated',
            'archived',
        ]


class CreateOrUpdateOrdinalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdinalTask
        fields = [
            'id',
            'name',
            'can_documents_be_invalidated',
            'labels',
            'archived',
        ]
        
        
class CreateOrUpdateEntityTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityTask
        fields = [
            'id',
            'name',
            'can_documents_be_invalidated',
            'labels',
            'archived',
        ]


class CreateOrUpdateTaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Task: CreateOrUpdateTaskSerializer,
        AudioRegionTask: CreateOrUpdateAudioRegionTaskSerializer,
        CategoricalTask: CreateOrUpdateCategoricalTaskSerializer,
        OrdinalTask: CreateOrUpdateOrdinalTaskSerializer,
        EntityTask: CreateOrUpdateEntityTaskSerializer,
        TextEditionTask: CreateOrUpdateTextEditionTaskSerializer,
        TranscriptionTask: CreateOrUpdateTranscriptionTaskSerializer,
    }


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
            'created_at',
            'updated_at',
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
            'created_at',
            'updated_at',
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
            'created_at',
            'updated_at',
        ]


class AudioRegionTaskSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField('get_labels')

    def get_labels(self, task):
        labels = task.labels.all()
        serializer = LabelPolymorphicSerializer(
            instance=labels,
            many=True,
            required=False,
            read_only=True
        )
        return serializer.data

    class Meta:
        model = AudioRegionTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'image',
            'html_guidelines',
            'archived',
            'color',
            'created_at',
            'updated_at',
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
            'created_at',
            'updated_at',
        ]


class NestedCategoricalTaskSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField('get_labels')

    def get_labels(self, task):
        labels = task.labels.all()
        serializer = LabelPolymorphicSerializer(
            instance=labels,
            many=True,
            required=False,
            read_only=True
        )
        return serializer.data

    class Meta:
        model = NestedCategoricalTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'image',
            'html_guidelines',
            'archived',
            'created_at',
            'updated_at',
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
            'created_at',
            'updated_at',
        ]


class TextEditionTaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = TextEditionTask
        fields = [
            'id',
            'name',
            'projects',
            'can_documents_be_invalidated',
            'labels',
            'image',
            'html_guidelines',
            'archived',
            'created_at',
            'updated_at',
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
            'created_at',
            'updated_at',
        ]


class TaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {  # TODO: generate this mapping automatically for automatic registration of plugins / task types
        Task: TaskSerializer,
        CategoricalTask: CategoricalTaskSerializer,
        OrdinalTask: OrdinalTaskSerializer,
        TranscriptionTask: TranscriptionTaskSerializer,
        LiveCorrectTask: LiveCorrectTaskSerializer,
        EntityTask: EntityTaskSerializer,
        TextEditionTask: TextEditionTaskSerializer,
        NestedCategoricalTask: NestedCategoricalTaskSerializer,
        AudioRegionTask: AudioRegionTaskSerializer,
    }
