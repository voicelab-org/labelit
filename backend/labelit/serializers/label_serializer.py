from rest_framework import serializers
from labelit.models import (
    Label,
    OrdinalLabel,
    TranscriptionLabel,
    LiveCorrectLabel,
    EntityLabel,
    TextEditionLabel,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from django.core.exceptions import ObjectDoesNotExist
from .timed_transcript_serializer import TimedTranscriptSerializer


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = [
            'id',
            'name',
            'task',
            'color'
        ]

class EntityLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityLabel
        fields = [
            'id',
            'name',
            'task',
            'color',
            'start_offset',
            'end_offset',
            'source_label'
        ]

class OrdinalLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdinalLabel
        fields = [
            'id',
            'name',
            'task',
            'color',
            'index',
        ]

    def create(self, validated_data):
        try:
            OrdinalLabel.objects.get(
                task=validated_data.get('task'),
                index=validated_data.get('index')
            )
            raise serializers.ValidationError(
                "Validation error: duplicate. A label with matching (label, task) already exists"
            )
        except ObjectDoesNotExist:
            pattern = OrdinalLabel(**validated_data)
            pattern.save()
        return pattern


class TranscriptionLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionLabel
        fields = [
            'id',
            'name',
            'task',
            'color',
            'transcript',
        ]


class TextEditionLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextEditionLabel
        fields = [
            'id',
            'name',
            'task',
            'color',
            'edited_text',
        ]



class LiveCorrectLabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = LiveCorrectLabel
        fields = [
            'id',
            'name',
            'task',
            'color',
            'timed_transcript',
        ]


class LiveCorrectLabelReadSerializer(serializers.ModelSerializer):
    timed_transcript = TimedTranscriptSerializer(read_only=True,)

    class Meta:
        model = LiveCorrectLabel
        fields = [
            'id',
            'name',
            'task',
            'color',
            'timed_transcript',
        ]


class LabelPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Label: LabelSerializer,
        OrdinalLabel: OrdinalLabelSerializer,
        TranscriptionLabel: TranscriptionLabelSerializer,
        LiveCorrectLabel: LiveCorrectLabelSerializer,
        EntityLabel: EntityLabelSerializer,
        TextEditionLabel: TextEditionLabelSerializer,
    }


class LabelPolymorphicReadSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Label: LabelSerializer,
        OrdinalLabel: OrdinalLabelSerializer,
        TranscriptionLabel: TranscriptionLabelSerializer,
        LiveCorrectLabel: LiveCorrectLabelReadSerializer,
        EntityLabel: EntityLabelSerializer,
        TextEditionLabel: TextEditionLabelSerializer,
    }
