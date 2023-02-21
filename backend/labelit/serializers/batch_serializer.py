from rest_framework import serializers
from labelit.models import Batch, SequenceBatch, BatchDocument, Document
from rest_polymorphic.serializers import PolymorphicSerializer
from .project_serializer import ProjectSerializer
from .dataset_serializer import DatasetSerializer


class SimpleBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = [
            "id",
            "name",
            "archived",
        ]


class BatchSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    dataset = DatasetSerializer()

    class Meta:
        model = Batch
        fields = [
            "id",
            "name",
            "dataset",
            "project",
            "annotators",
            "documents",
            "num_documents",
            "num_annotators_per_document",
            "annotation_mode",
            "annotation_limit",
            "archived",
        ]


class FlatBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = [
            "id",
            "name",
            "dataset",
            "project",
            "annotators",
            "documents",
            "num_documents",
            "num_annotators_per_document",
            "annotation_mode",
            "annotation_limit",
            "archived",
        ]

    def create(self, validated_data):
        annotators = validated_data.pop("annotators")
        batch = Batch(**validated_data)
        batch.save()
        batch.annotators.set(annotators)
        free_documents = Document.objects.filter(
            dataset=batch.dataset,
        ).exclude(
            id__in=BatchDocument.objects.filter(
                batch__in=batch.project.batches.all()
            ).values("document_id")
        )
        documents_to_add = free_documents[: batch.num_documents]
        for document in documents_to_add:
            BatchDocument.objects.create(batch=batch, document=document)

        return batch


class SequenceBatchSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = SequenceBatch
        fields = [
            "id",
            "name",
            "dataset",
            "project",
            "annotators",
            "sequences",
            "num_sequences",
            "num_annotators_per_document",
            "annotation_mode",
            "annotation_limit",
            "archived",
        ]
        extra_kwargs = {"project": {"write_only": True}}


class BatchPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Batch: BatchSerializer,
        SequenceBatch: SequenceBatchSerializer,
    }
