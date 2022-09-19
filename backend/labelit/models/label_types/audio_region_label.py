from django.db import models
from labelit.models.label import Label


class AudioRegionLabel(Label):
    start = models.FloatField(
        'start time in seconds',
    )
    end = models.FloatField(
        'end time in seconds',
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<AudioRegionLabel ({}): {}>".format(self.pk, self.name)
