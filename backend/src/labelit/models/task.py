from django.db import models
from polymorphic.models import PolymorphicModel


class Task(PolymorphicModel):
    name = models.CharField(
        max_length=200,
    )
    html_guidelines = models.TextField(
        default="<h2>Customize guidelines</h2>",
        blank=True,
    )
    can_documents_be_invalidated = models.BooleanField(
        """
        If true, annotators can tag a document as 'invalid'
        and skip annotation.
        """,
        default=True,
    )
    image = models.ImageField(upload_to="task-images", blank=True, null=True)

    archived = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<Task ({}): {}>".format(self.pk, self.name)

    def validate_labels(self, labels, is_final):
        raise NotImplementedError

    def get_agreement_stats(self, batch):
        raise NotImplementedError
