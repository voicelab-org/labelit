from rest_framework import serializers
from labelit.serializers.document_serializer import MinimalDocumentSerializer
from labelit.serializers import TaskPolymorphicSerializer, TaskSerializer
from labelit.serializers import ExportedBatchSerializer
from labelit.models import Project, BatchDocument, Document


class ExportedProjectSerializer(serializers.ModelSerializer):

    tasks = TaskPolymorphicSerializer(many=True, required=False)
    num_documents = serializers.SerializerMethodField()
    num_done_documents = serializers.SerializerMethodField()
    num_done_batches = serializers.SerializerMethodField()
    batches = ExportedBatchSerializer(many=True, required=False)
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'is_audio_annotated',
            'is_text_annotated',
            'are_sequences_annotated',
            'tasks',
            'num_documents',
            'num_done_documents',
            'num_done_batches',
            'batches',
            'archived',
            'documents'
        ]

    def get_num_documents(self, obj):
        return obj.get_num_documents()

    def get_documents(self, obj):
        batch_documents = BatchDocument.objects.filter(
            batch__in=obj.batches.all(),
        )
        documents = Document.objects.filter(
            id__in=batch_documents.values_list("document_id", flat=True)
        )
        serializer = MinimalDocumentSerializer(documents, many=True)
        return serializer.data

    def get_num_done_documents(self, obj):
        return obj.get_num_done_documents()

    def get_num_done_batches(self, obj):
        return obj.get_num_done_batches()
