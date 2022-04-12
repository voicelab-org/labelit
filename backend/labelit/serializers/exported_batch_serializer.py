from rest_framework import serializers
from labelit.models import Batch, SequenceBatch, BatchDocument, Document
from .dataset_serializer import DatasetSerializer
from .annotation_serializer import AnnotationWithLabelsSerializer
from .user_serializer import UserSerializer


class ExportedBatchSerializer(serializers.ModelSerializer):
    dataset = DatasetSerializer()
    annotators = UserSerializer(many=True, required=False,)
    annotations = AnnotationWithLabelsSerializer(many=True, required=False,)

    class Meta:
        model = Batch
        fields = [
            'id',
            'name',
            'dataset',
            'project',
            'annotators',
            'annotations',
            'documents',
            'num_documents',
            'num_annotators_per_document',
            'annotation_mode',
            'annotation_limit',
            'archived',
        ]
