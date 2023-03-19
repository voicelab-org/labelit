from rest_framework import serializers
from labelit.models import (
    Task,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from .label_serializer import LabelPolymorphicSerializer
from labelit.serializers.task_serializers import (
    AudioRegionTaskSerializer,
    CreateOrUpdateAudioRegionTaskSerializer,
    CreateOrUpdateCategoricalTaskSerializer,
    CategoricalTaskSerializer,
    EntityTaskSerializer,
    CreateOrUpdateEntityTaskSerializer,
    LiveCorrectTaskSerializer,
    NestedCategoricalTaskSerializer,
    OrdinalTaskSerializer,
    CreateOrUpdateOrdinalTaskSerializer,
    TextEditionTaskSerializer,
    CreateOrUpdateTextEditionTaskSerializer,
    TranscriptionTaskSerializer,
    CreateOrUpdateTranscriptionTaskSerializer,
)


# TODO: DRY the code


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


class CreateOrUpdateTaskPolymorphicSerializer(PolymorphicSerializer):

    @staticmethod
    def _get_mapping():
        return {
            Task: CreateOrUpdateTaskSerializer,
            AudioRegionTask: CreateOrUpdateAudioRegionTaskSerializer,
            CategoricalTask: CreateOrUpdateCategoricalTaskSerializer,
            OrdinalTask: CreateOrUpdateOrdinalTaskSerializer,
            EntityTask: CreateOrUpdateEntityTaskSerializer,
            TextEditionTask: CreateOrUpdateTextEditionTaskSerializer,
            TranscriptionTask: CreateOrUpdateTranscriptionTaskSerializer,
        }

    model_serializer_mapping = CreateOrUpdateTaskPolymorphicSerializer._get_mapping()


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


class TaskPolymorphicSerializer(PolymorphicSerializer):

    def _get_mapping(self):
        return {
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

    model_serializer_mapping =TaskPolymorphicSerializer._get_mapping()
