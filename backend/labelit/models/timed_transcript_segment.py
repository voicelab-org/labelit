from django.db import models


class TimedTranscriptSegment(models.Model):

    timed_transcript = models.ForeignKey(
        "labelit.TimedTranscript",
        on_delete=models.CASCADE,
        related_name="segments",
    )

    transcript = models.TextField(
        "The transcript to correct",
        null=True,
        blank=True,
    )

    start_time = models.FloatField(
        "The start time relative to beginning of audio",
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<TimedTranscriptSegment ({})>".format(
            self.pk,
        )
