from rest_framework import serializers
from labelit.serializers import TaskPolymorphicSerializer, TaskSerializer, MinimalDocumentSerializer
from labelit.serializers import ExportedBatchSerializer
from labelit.models import Project


class ExportedProjectSerializer(serializers.ModelSerializer):

    tasks = TaskPolymorphicSerializer(many=True, required=False)
    num_documents = serializers.SerializerMethodField()
    num_done_documents = serializers.SerializerMethodField()
    num_done_batches = serializers.SerializerMethodField()
    batches = ExportedBatchSerializer(many=True, required=False)
    documents = MinimalDocumentSerializer(many=True, required=False)

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

    def get_num_done_documents(self, obj):
        return obj.get_num_done_documents()

    def get_num_done_batches(self, obj):
        return obj.get_num_done_batches()
