from rest_framework import serializers
from labelit.models import Annotation, Label
from .user_serializer import UserSerializer
from .label_serializer import LabelPolymorphicReadSerializer


class AnnotationWithLabelsSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicReadSerializer(many=True)
    text = serializers.CharField(source="document.text")
    audio_filename = serializers.CharField(source="document.audio_filename")

    class Meta:
        model = Annotation
        fields = [
            "annotator",
            "batch",
            "labels",
            "document",
            "audio_filename",
            "text",
            "task",
            "project",
            "document_sequence",
            "is_done",
            "id",
            "has_qa_validated",
            "has_qa_invalidated",
            "is_resubmitted",
            "qa_invalidation_comment",
            "time",
        ]


class AnnotationSerializer(serializers.ModelSerializer):
    labels = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Label.objects
    )

    class Meta:
        model = Annotation
        fields = [
            "annotator",
            "batch",
            "labels",
            "document",
            "task",
            "project",
            "document_sequence",
            "is_done",
            "id",
            "has_qa_validated",
            "has_qa_invalidated",
            "is_resubmitted",
            "qa_invalidation_comment",
            "time",
        ]

    def validate(self, attrs):
        attrs["task"].validate_labels(attrs["labels"], attrs["is_done"])
        return attrs


class AnnotationWithUserSerializer(serializers.ModelSerializer):
    annotator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Annotation
        fields = [
            "annotator",
            "batch",
            "labels",
            "document",
            "task",
            "project",
            "document_sequence",
            "is_done",
            "id",
            "has_qa_validated",
            "has_qa_invalidated",
            "is_resubmitted",
            "qa_invalidation_comment",
            "time",
        ]
