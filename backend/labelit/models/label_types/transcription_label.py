from django.db import models
from labelit.models.label import Label


class TranscriptionLabel(Label):
    transcript = models.TextField(
        'the transcript',
        default="",
        blank=True,
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<TranscriptionLabel ({}): {}>".format(self.pk, self.transcript)
