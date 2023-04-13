from django.db import models
from labelit.models.label import Label


CHOICES = range(0, 101)


class RealtimeVideoDimensionalLabel(Label):
    sequence = models.JSONField(
        verbose_name="The sequence of <video time, dimensional value> pairs"
    )
    summative = models.IntegerField(
        verbose_name="The summative (synthetic) annotation associated with the entire video"
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<RealtimeVideoDimensionalLabel ({}): {}>".format(self.pk, self.name)
