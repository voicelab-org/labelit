from django.db import models
from django.conf import settings


class Annotation(models.Model):
    is_done = models.BooleanField(
        "If true, annotation is confirmed",
        default=False
    )
    annotator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        'labelit.Task',  # denormalized
        on_delete=models.CASCADE
    )
    batch = models.ForeignKey(
        'labelit.Batch',
        on_delete=models.CASCADE,
        related_name='annotations'
    )
    labels = models.ManyToManyField(
        'labelit.Label',
        related_name="annotations",
    )
    document = models.ForeignKey(
        'labelit.Document',
        on_delete=models.CASCADE,
        related_name='annotations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_qa_validated = models.BooleanField(
        'Whether QA has marked annotation as valid',
        default=False,
    )
    has_qa_invalidated = models.BooleanField(
        'Whether QA has marked annotation as invalid',
        default=False,
    )
    is_resubmitted = models.BooleanField(
        'Whether annotator has resubmitted the annotation following invalidation by QA',
        default=False,
    )
    qa_invalidation_comment = models.CharField(
        "The comment accompanying a QA's invalidation",
        max_length=500,
        null=True,
        blank=True,
    )
    time = models.IntegerField(
        "The time (ms) taken to annotate the document (possibly including other annotations for other tasks)",
        default=0,
    )
    # BEGIN denormalized fields
    project = models.ForeignKey(
        'labelit.Project',  # denormalized
        on_delete=models.CASCADE
    )
    document_sequence = models.ForeignKey(
        'labelit.DocumentSequence',  # denormalized
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # END denormalized fields

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<Annotation ({}): task: {} annotator: {}>".format(
            self.pk,
            self.task,
            self.annotator
        )
