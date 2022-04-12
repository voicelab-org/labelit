from django.db import models
from .abstract_batch_unit import BatchUnit
from .annotation import Annotation
import math


class BatchDocument(BatchUnit):
    document = models.ForeignKey(
        'labelit.Document',
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<BatchDocument: {}%{}>".format(self.batch, self.document)

    def update_annotation_progress_statistics(self, saved_annotation=None):
        """
        Updates denormalized fields on the BatchDocument object.

        Args:
            annotation: the newly created annotation
        """

        annotations = Annotation.objects.filter(
            # document=saved_annotation.document,
            document=self.document,
            batch=self.batch,
        )
        done_annotations_on_doc = annotations.filter(
            is_done=True
        )

        num_tasks = self.batch.project.tasks.all().count()
        self.num_done_annotators = math.floor(
            done_annotations_on_doc.count() / num_tasks
        )
        self.num_annotators = annotations.values('annotator_id').distinct().count()
        self.save()
