from django.db import models
from labelit.models.task import Task
from zope.dottedname.resolve import resolve


class LiveCorrectTask(Task):

    validator = models.CharField(
        "Dotted path to the validator class",
        max_length=500,
        default='labelit.validators.base_transcription_validator.BaseTranscriptionValidator',
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<LiveCorrectTask ({})>".format(self.pk,)

    def validate_labels(
            self,
            labels,
            is_final
    ):
        timed_transcript = labels[0].timed_transcript
        for segment in timed_transcript.segments.all():
            resolve(self.validator)().validate(segment.transcript)

    def get_batch_stats(self, batch):
        stats = {}
        return stats

    def get_agreement_stats(self, batch):
        raise NotImplementedError
