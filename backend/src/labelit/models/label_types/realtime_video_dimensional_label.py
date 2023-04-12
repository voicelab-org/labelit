from django.db import models
from labelit.models.label import Label

DIMENSIONAL_ANNOTATION_CHOICES = list(range(0, 101))


class RealtimeVideoDimensionalLabel(Label):
    realtime_sequence = models.JSONField(
        "The realtime sequence of (frame time, dimensional annotation) pairs",
        blank=True,
    )
    summative_annotation = (
        models.IntegerField(
            verbose_name="The annotation of the entire ",
            choices=DIMENSIONAL_ANNOTATION_CHOICES,
        ),
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<RealtimeVideoDimensionalLabel ({})>".format(self.pk)
