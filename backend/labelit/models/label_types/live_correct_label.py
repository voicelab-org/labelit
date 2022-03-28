from django.db import models
from labelit.models.label import Label


class LiveCorrectLabel(Label):
    timed_transcript = models.ForeignKey(
        'labelit.TimedTranscript',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<LiveCorrectLabel ({}): {}>".format(self.pk, self.timed_transcript)
