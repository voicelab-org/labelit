from django.db import models


class TimedTranscript(models.Model):
    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<TimedTranscript ({})>".format(
            self.pk,
        )
