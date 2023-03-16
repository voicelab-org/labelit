from django.db import models


class LexiconEntry(models.Model):
    lexicon = models.ForeignKey(
        "labelit.Lexicon",
        related_name="entries",
        on_delete=models.CASCADE,
    )
    entry = models.CharField(
        max_length=500,
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<LexiconEntry {}: {}>".format(self.pk, self.entry)
