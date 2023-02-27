from django.test import TestCase
from django.contrib.auth import get_user_model

from labelit.models import (
    OrdinalTask,
    Project,
    SequenceBatch,
    Document,
    Dataset,
    Annotation,
    DocumentSequence,
    BatchDocumentSequence,
    Batch,
)
import math


class SequenceBatchModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Feelin",
        )
        self.task1 = OrdinalTask.objects.create(
            name="Valence scale",
        )
        self.project.tasks.add(self.task1)
        self.dataset = Dataset.objects.create(name="IMDB")
        self.doc_seq1 = DocumentSequence.objects.create(
            dataset=self.dataset, num_documents=3
        )
        self.doc1 = Document.objects.create(
            text="lovedit",
            dataset=self.dataset,
            document_sequence=self.doc_seq1,
            sequence_index=0,
        )
        self.doc2 = Document.objects.create(
            text="hatedit",
            dataset=self.dataset,
            document_sequence=self.doc_seq1,
            sequence_index=1,
        )
        self.doc3 = Document.objects.create(
            text="kindaenjoyedit",
            dataset=self.dataset,
            document_sequence=self.doc_seq1,
            sequence_index=2,
        )
        self.doc_seq2 = DocumentSequence.objects.create(
            dataset=self.dataset, num_documents=1
        )
        self.doc4 = Document.objects.create(
            text="toleratedit",
            dataset=self.dataset,
            document_sequence=self.doc_seq2,
            sequence_index=0,
        )

        self.batch1 = SequenceBatch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            project=self.project,
            num_annotators_per_document=2,
            num_sequences=2,
            num_documents=4,
        )
        self.batch1.annotation_mode = self.batch1.EVEN
        self.batch1.sequences.add(self.doc_seq1)
        self.batch1.sequences.add(self.doc_seq2)
        self.batch1.save()

        self.user1 = get_user_model().objects.create(email="janedoe@labelit")
        self.user2 = get_user_model().objects.create(email="juggernaut@labelit")
        self.batch1.annotators.add(self.user1)
        self.batch1.annotators.add(self.user2)

        self.annotation1 = Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )

    def test_get_annotation_limit_with_annotation_mode_set_to_even(self):
        Annotation.objects.all().delete()

        self.assertEqual(self.batch1.get_annotation_limit(), 2)

    def test_get_annotation_limit_with_annotation_mode_set_to_all_you_can_annotate(
        self,
    ):
        self.batch1.annotation_mode = self.batch1.ALL_YOU_CAN_ANNOTATE
        Annotation.objects.all().delete()

        self.assertEqual(self.batch1.get_annotation_limit(), math.inf)
        self.batch1.annotation_limit = 1
        self.assertEqual(self.batch1.get_annotation_limit(), 1)

    def test_get_next_document_to_annotate(self):
        self.assertEqual(
            self.batch1.get_next_document_to_annotate(self.user1), self.doc2
        )
        self.annotation2 = Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc2,
            project=self.batch1.project,
            batch=self.batch1,
            is_done=False,
        )

        self.assertEqual(
            self.batch1.get_next_document_to_annotate(self.user1), self.doc2
        )

        self.annotation2.is_done = True
        self.annotation2.save()

        self.assertEqual(
            self.batch1.get_next_document_to_annotate(self.user1), self.doc3
        )

        self.annotation4 = Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc3,
            project=self.batch1.project,
            batch=self.batch1,
            is_done=True,
        )

        self.assertEqual(
            self.batch1.get_next_document_to_annotate(self.user1), self.doc4
        )

        # self.annotation4.delete()
        self.batch1.annotation_mode = self.batch1.ALL_YOU_CAN_ANNOTATE
        self.batch1.annotation_limit = 1
        self.batch1.save()
        self.annotation2.is_done = True
        self.annotation2.save()
        self.assertEqual(self.batch1.get_next_document_to_annotate(self.user1), None)

    def test_get_num_done_units(self):
        self.assertEqual(self.batch1.get_num_done_units(), 0)
        Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc2,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc3,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.assertEqual(self.batch1.get_num_done_units(), 0)
        Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.assertEqual(self.batch1.get_num_done_units(), 0)
        Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc2,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc3,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.assertEqual(self.batch1.get_num_done_units(), 1)
        Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc4,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc4,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.assertEqual(self.batch1.get_num_done_units(), 2)

    def test_get_remaining_units_in_dataset(self):
        self.assertEqual(
            SequenceBatch.get_remaining_units_in_dataset(self.project, self.dataset), 0
        )
        DocumentSequence.objects.create(dataset=self.dataset, num_documents=2)
        self.assertEqual(
            SequenceBatch.get_remaining_units_in_dataset(self.project, self.dataset), 1
        )

    def test_get_next_document_to_qa(self):
        self.batch1.get_next_document_to_qa()
