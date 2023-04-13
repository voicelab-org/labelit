from labelit.models import Task
from django.db import models
from zope.dottedname.resolve import resolve


class TranscriptionTask(Task):
    validator = models.CharField(
        "Dotted path to the validator class",
        max_length=500,
        default="labelit.validators.base_transcription_validator.BaseTranscriptionValidator",
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<TranscriptionTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(
        self,
        labels,
        is_final,
    ):
        resolve(self.validator)().validate(labels[0].transcript)

    def get_agreement_stats(self, batch):
        return {}
