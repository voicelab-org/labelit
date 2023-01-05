from django.db import models
from labelit.models.label import Label


class NestedCategoricalLabel(Label):

    parent_label = models.ForeignKey(
        "labelit.NestedCategoricalLabel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="nested_children_labels",
    )

    single_child_select = models.BooleanField(
        "Whether only one child label can be selected at any time",
        default=True,
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<NestedCategoricalLabel ({}): {}>".format(self.pk, self.name)
