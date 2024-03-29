from django.db import models
import os
from django.db.models import JSONField
from django.core.serializers.json import DjangoJSONEncoder


class Document(models.Model):
    text = models.TextField(
        "The text content of this document",
        blank=True,
        null=True,
    )
    video_filename = models.CharField(
        "The video file name", max_length=3000, default=None, blank=True, null=True
    )
    audio_filename = models.CharField(
        "The audio file name", max_length=3000, default=None, blank=True, null=True
    )
    audio_duration = models.IntegerField(
        "Length (ms) of audio if exists",
        default=0,
    )
    dataset = models.ForeignKey(
        "labelit.Dataset", on_delete=models.CASCADE, related_name="documents"
    )
    document_sequence = models.ForeignKey(
        "labelit.DocumentSequence",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sequence_index = models.IntegerField(
        "Index (order) of document in sequence", null=True, blank=True
    )
    timed_transcript = models.ForeignKey(
        "labelit.TimedTranscript",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    metadata = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)

    @property
    def audio_waveform_json(self):
        return os.path.splitext(self.audio_filename)[0] + "_waveform.json"

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<Document: {} {}>".format(self.pk, self.audio_filename)
