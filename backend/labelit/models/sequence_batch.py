from .batch import Batch
from django.db import models
from .batch_document_sequence import BatchDocumentSequence
from .document import Document
from .annotation import Annotation
import math


class SequenceBatch(Batch):
    sequences = models.ManyToManyField(
        'labelit.DocumentSequence',
        through="labelit.BatchDocumentSequence"
    )
    num_sequences = models.IntegerField(
        "The number of document sequences in this batch (denormalized field)",
        default=1
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<SequenceBatch ({}): {}>".format(self.pk, self.name)

    def get_batch_unit(self, document):
        return BatchDocumentSequence.objects.get(
            document_sequence=document.document_sequence,
            batch=self
        )

    def get_annotation_limit(self):
        if self.annotation_mode == self.EVEN:
            assert(self.annotation_limit is None)
            return math.floor(
                self.num_sequences * self.num_annotators_per_document / self.annotators.all().count()
            )
        else:
            if self.annotation_limit is not None:
                return self.annotation_limit
        return math.inf

    def get_next_document_to_annotate(self, user):

        in_progress_annotations = Annotation.objects.filter(
            batch=self,
            annotator=user,
            is_done=False
        )
        if in_progress_annotations.count() > 0:
            return in_progress_annotations.first().document

        # find any document sequence only partly annotated by annotator
        num_tasks = self.project.tasks.all().count()
        partly_annotated_sequences = Annotation.objects.filter(
            batch=self,
            annotator=user,
            is_done=True
        ).values(
            'document__document_sequence',
        ).annotate(
            num_annotations=models.Count('id', distinct=True),
            max_index=models.Max('document__sequence_index')
        ).filter(
            num_annotations__lt=num_tasks * models.F('document__document_sequence__num_documents')
        )
        partly_annotated_sequences = list(partly_annotated_sequences)
        assert(len(partly_annotated_sequences) <= 1)
        if len(partly_annotated_sequences):
            seq = partly_annotated_sequences[0]
            return Document.objects.get(
                document_sequence=seq['document__document_sequence'],
                sequence_index=seq['max_index'] + 1,
            )

        annotated_seq_ids = set(Annotation.objects.filter(
            batch=self,
            annotator=user,
            is_done=True,
            document__document_sequence__in=self.sequences.all().values('id')
        ).values_list('document__document_sequence_id'))

        assert(not len(annotated_seq_ids) > self.get_annotation_limit())
        if len(annotated_seq_ids) >= self.get_annotation_limit():
            return None

        incomplete_batch_doc_seqs = BatchDocumentSequence.objects.filter(
            batch=self,
            num_annotators__lt=self.num_annotators_per_document,
        )
        for incomplete_batch_doc_seq in incomplete_batch_doc_seqs:
            documents = Document.objects.filter(
                document_sequence=incomplete_batch_doc_seq.document_sequence
            ).exclude(
                id__in=Annotation.objects.filter(
                    annotator=user,
                    batch=self,
                    document__document_sequence=incomplete_batch_doc_seq.document_sequence
                ).values('document__id')
            )
            if documents.count() > 0:
                return documents.order_by('sequence_index').first()

        return None

    def get_num_done_units(self):
        return BatchDocumentSequence.objects.filter(
            batch=self,
            num_done_annotators=self.num_annotators_per_document
        ).count()

    def get_total_units(self):
        return self.num_sequences

    @staticmethod
    def get_remaining_units_in_dataset(project, dataset):
        return dataset.document_sequences.all().count() - BatchDocumentSequence.objects.filter(
            document_sequence__dataset=dataset,
            batch__in=project.batches.all()
        ).count()

    def get_num_done_annotations_for_user(self, user):
        raise NotImplementedError