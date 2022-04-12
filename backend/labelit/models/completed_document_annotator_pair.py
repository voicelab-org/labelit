from django.db import models
from django.conf import settings


"""
This entire class is denormalized
"""
class CompletedDocumentAnnotatorPair(models.Model):
    annotator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    document = models.ForeignKey(
        'labelit.Document',  # denormalized
        on_delete=models.CASCADE
    )
    batch = models.ForeignKey(
        'labelit.Batch',
        on_delete=models.CASCADE,
        related_name='completed_document_annotator_pairs'
    )
    project = models.ForeignKey(
        'labelit.Project',
        related_name="completed_document_annotator_pairs",
        on_delete=models.CASCADE,
        default=None,
    )
    annotation_time = models.IntegerField(
        'Time it took to annotate the document (ms)',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'labelit'
        unique_together = [['annotator', 'document', 'batch']]

    def __str__(self):
        return "<CompletedDocumentAnnotatorPair ({}): document: {} annotator: {} project: {}>".format(
            self.pk,
            self.document,
            self.annotator,
            self.project,
        )
