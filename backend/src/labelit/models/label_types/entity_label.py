from django.db import models
from labelit.models.label import Label


class EntityLabel(Label):
    start_offset = models.IntegerField(
        "start offset of the entity in the document text",
        default=0,
    )
    end_offset = models.IntegerField(
        "end offset of the entity in the document text",
        default=0,
    )

    # for easier tracking
    source_label = models.ForeignKey(
        "labelit.Label",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children_labels",
    )  # TODO: remove, no longer needed

    # toy comment TODO remove

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<EntityLabel ({}): {}>".format(self.pk, self.name)
