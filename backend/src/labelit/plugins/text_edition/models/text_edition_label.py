from django.db import models
from labelit.models.label import Label


class TextEditionLabel(Label):
    edited_text = models.TextField(
        "the edited document text",
        default="",
        blank=True,
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<TextEditionLabel ({}): {}>".format(self.pk, self.edited_text)
