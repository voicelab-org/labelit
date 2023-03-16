from rest_framework import serializers
from labelit.models import DocumentSequence


class DocumentSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSequence
        fields = ["dataset", "num_documents"]
