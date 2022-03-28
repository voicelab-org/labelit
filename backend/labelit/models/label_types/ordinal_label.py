from django.db import models
from labelit.models.label import Label


class OrdinalLabel(Label):
    index = models.IntegerField(
        'the index of this label in the ordinal scale',
        default=0
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<OrdinalLabel ({}): {}>".format(self.pk, self.name)
