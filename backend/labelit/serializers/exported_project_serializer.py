from rest_framework import serializers
from labelit.serializers.document_serializer import MinimalDocumentSerializer
from labelit.serializers import TaskPolymorphicSerializer, TaskSerializer
from labelit.serializers import ExportedBatchSerializer
from labelit.models import Project, BatchDocument, Document

from django.db.models import Case, When, Value, IntegerField, F

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
        # batch_documents = BatchDocument.objects.filter(
        #     batch__in=obj.batches.all(),
        # )
        batch_documents = BatchDocument.objects.filter(
            batch__in=obj.batches.all(),
        ).annotate(is_done=Case(
            When(
                num_done_annotators=F('batch__num_annotators_per_document'),
                then=Value(1)
            ),
            default=Value(0),
            output_field=IntegerField()
        )).filter(is_done=True)
        documents = Document.objects.filter(
            id__in=batch_documents.values("document_id")
        )
        serializer = MinimalDocumentSerializer(documents, many=True)
        return serializer.data

    def get_num_done_documents(self, obj):
        return obj.get_num_done_documents()

    def get_num_done_batches(self, obj):
        return obj.get_num_done_batches()
