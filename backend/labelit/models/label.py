from django.db import models
from ..utils.color_generator import random_dark_color
from polymorphic.models import PolymorphicModel


class Label(PolymorphicModel):
    task = models.ForeignKey(
        'labelit.Task',
        on_delete=models.CASCADE,
        related_name="labels",
        null=True,
    )
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    color = models.CharField(
        "The rbg() color string, e.g. rgb(255,231,78)",
        default=random_dark_color,
        max_length=50
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<Label ({}): {}>".format(self.pk, self.name)
