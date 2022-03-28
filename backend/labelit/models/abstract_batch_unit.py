from django.db import models
from django.core.exceptions import ValidationError


# the Unit can be a document or a document sequence
class BatchUnit(models.Model):
    batch = models.ForeignKey(
        'labelit.Batch',
        on_delete=models.CASCADE,
    )
    # BEGIN denormalized fields
    num_done_annotators = models.IntegerField(
        """
        Number of annotation sets completed by annotators.
        An annotation set is complete when exactly one annotation by the annotator exists
        for each task in the project for every document for the unit.
        For a Batch, the unit is the document itself.
        For a SequenBatch, the unit is the document sequence.
        """,
        default=0
    )
    num_annotators = models.IntegerField(
        """
        Number of annotators who have annotated or are currently annotating
        the unit
        """,
        default=0
    )
    # END denormalized fields

    class Meta:
        app_label = 'labelit'
        abstract = True

    def __str__(self):
        return "<BatchUnit for batch: {}>".format(self.batch)

    def update_annotation_progress_statistics(self, saved_annotation=None):
        raise NotImplementedError
