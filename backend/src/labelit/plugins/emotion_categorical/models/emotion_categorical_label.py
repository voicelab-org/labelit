from django.db import models
from labelit.models.label import Label


class EmotionCategoricalLabel(Label):
    tags_with_intensities = models.JSONField(
        verbose_name="The collection of <tag, intensity> pairs"
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<EmotionCategoricalLabel ({}): {}>".format(self.pk, self.name)
