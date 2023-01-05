from django.db import models
from .abstract_batch_unit import BatchUnit
from .annotation import Annotation
from .batch_document import BatchDocument
import math


class BatchDocumentSequence(BatchUnit):

    batch = models.ForeignKey("labelit.SequenceBatch", on_delete=models.CASCADE)

    document_sequence = models.ForeignKey(
        "labelit.DocumentSequence",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<BatchDocumentSequence: {}%{}>".format(
            self.batch, self.document_sequence
        )

    def update_annotation_progress_statistics(self, saved_annotation=None):
        annotations = Annotation.objects.filter(
            document__document_sequence=saved_annotation.document.document_sequence,
        )
        done_annotations_on_docs_in_seq = annotations.filter(is_done=True)
        num_tasks = self.batch.project.tasks.all().count()

        self.num_done_annotators = math.floor(
            done_annotations_on_docs_in_seq.count()
            / (num_tasks * saved_annotation.document.document_sequence.num_documents)
        )
        self.num_annotators = annotations.values("annotator_id").distinct().count()

        """
        for batch_doc in BatchDocument.objects.filter(
            batch=self.batch,
        )
        """

        self.save()
