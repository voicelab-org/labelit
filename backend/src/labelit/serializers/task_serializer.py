from rest_framework import serializers
from labelit.models import (
    Task,
    LiveCorrectTask,
    AudioRegionTask,
    OrdinalTask,
    CategoricalTask,
    NestedCategoricalTask,
    TextEditionTask,
    TranscriptionTask,
    EntityTask,
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

def _get_mapping(
        is_create_or_update=False,
):
    if is_create_or_update:
        return {
            Task: CreateOrUpdateTaskSerializer,
            AudioRegionTask: CreateOrUpdateAudioRegionTaskSerializer,
            CategoricalTask: CreateOrUpdateCategoricalTaskSerializer,
            OrdinalTask: CreateOrUpdateOrdinalTaskSerializer,
            EntityTask: CreateOrUpdateEntityTaskSerializer,
            TextEditionTask: CreateOrUpdateTextEditionTaskSerializer,
            TranscriptionTask: CreateOrUpdateTranscriptionTaskSerializer,
        }
    else:
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

create_or_update_mappping = _get_mapping(is_create_or_update=True)


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


mapping = _get_mapping()

class TaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = mapping
