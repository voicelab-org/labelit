import math

from django.contrib.auth import get_user_model
from django.test import TestCase

from labelit.models import (
    Annotation,
    Batch,
    CategoricalTask,
    Dataset,
    Document,
    OrdinalTask,
    Project,
    Task,
)
from labelit.tests import TestSetup


class BatchModelTests(TestSetup, TestCase):
    # fixtures = ['test_data']

    def setUp(self):
        Annotation.objects.all().delete()
        super().setUp()

        self.annotation1 = Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.annotation2 = Annotation.objects.create(
            annotator=self.user1,
            task=self.task1,
            document=self.doc2,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.ANNOTATION_MODES = self.batch1.ANNOTATION_MODES
        self.EVEN = self.batch1.EVEN
        self.ALL_YOU_CAN_ANNOTATE = self.batch1.ALL_YOU_CAN_ANNOTATE

    def test_get_annotation_limit_with_annotation_mode_set_to_even(self):
        batch = Batch.objects.create(
            name="Somebatch",
            dataset=self.dataset,
            project=self.project,
            num_annotators_per_document=2,
            num_documents=20,
            annotation_mode=self.EVEN,
        )
        batch.annotators.add(self.user1)
        batch.annotators.add(self.user2)
        self.assertEqual(batch.get_annotation_limit(), 20)

    def test_get_annotation_limit_with_annotation_mode_set_to_all_you_can_annotate(
        self,
    ):
        batch = Batch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            project=self.project,
            num_annotators_per_document=2,
            num_documents=20,
            annotation_mode=self.ALL_YOU_CAN_ANNOTATE,
        )
        batch.annotators.add(self.user1)
        batch.annotators.add(self.user2)
        self.assertEqual(batch.get_annotation_limit(), math.inf)

        # adding limit
        batch.annotation_limit = 7
        self.assertEqual(batch.get_annotation_limit(), 7)

    def test_get_next_document_to_annotate_in_even_mode(self):
        self.assertTrue(
            self.batch1.get_next_document_to_annotate(self.user2) is not None
        )
        self.assertTrue(
            self.batch1.get_next_document_to_annotate(self.user2)
            in [self.doc1, self.doc2, self.doc3]
        )

    def test_get_next_document_to_annotate_in_all_you_can_annotate_mode(self):
        self.batch1.annotation_mode = self.batch1.ALL_YOU_CAN_ANNOTATE
        self.assertTrue(
            self.batch1.get_next_document_to_annotate(self.user2) is not None
        )
        self.assertTrue(
            self.batch1.get_next_document_to_annotate(self.user2)
            in [self.doc1, self.doc2, self.doc3]
        )

        Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        Annotation.objects.create(
            annotator=self.user2,
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.batch1.annotation_limit = 1
        self.assertTrue(self.batch1.get_next_document_to_annotate(self.user2) is None)

    def test_get_num_done_units(self):
        self.assertEqual(self.batch1.get_num_done_units(), 0)
        Annotation.objects.create(
            annotator=self.user1,
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )

        Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )

        Annotation.objects.create(
            annotator=self.user2,
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.assertEqual(self.batch1.get_num_done_units(), 1)

    def test_get_num_done_annotations_for_user(self):
        self.assertEqual(
            self.batch1.get_num_done_annotations_for_user(
                self.user1,
            ),
            1,
        )
        self.assertEqual(
            self.batch1.get_num_done_annotations_for_user(
                self.user2,
            ),
            0,
        )

    def test_get_remaining_units_in_dataset(self):
        self.assertEqual(
            Batch.get_remaining_units_in_dataset(self.project, self.dataset), 0
        )
        Document.objects.create(
            text="a bad movie if there ever there was one", dataset=self.dataset
        )
        self.assertEqual(
            Batch.get_remaining_units_in_dataset(self.project, self.dataset), 1
        )

        # availability is per-project
        project2 = Project.objects.create(
            name="my other project",
            target_deadline="2023-03-08",
            target_num_documents=100,
        )
        batch2 = Batch.objects.create(
            name="Batch 2",
            dataset=self.dataset,
            project=project2,
            num_annotators_per_document=2,
            num_documents=2,
        )
        batch2.documents.add(self.doc1)
        batch2.save()
        self.assertEqual(
            Batch.get_remaining_units_in_dataset(project2, self.dataset), 3
        )

    def test_get_document_to_undo(self):
        Annotation.objects.create(
            annotator=self.user1,
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.assertEqual(self.batch1.get_document_to_undo(self.user1), self.doc1)

    def test_get_next_document_to_qa(self):
        annotation3 = Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )

        self.assertEqual(self.batch1.get_next_document_to_qa(), None)

        annotation4 = Annotation.objects.create(
            annotator=self.user1,
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )

        annotation5 = Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )

        annotation6 = Annotation.objects.create(
            annotator=self.user2,
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.assertEqual(self.batch1.get_next_document_to_qa(), self.doc1)

        # validate doc1
        Annotation.objects.filter(
            document=self.doc1,
        ).update(has_qa_validated=True)

        self.assertEqual(self.batch1.get_next_document_to_qa(), None)

    def test_get_next_document_to_review(self):
        # no QA done yet
        self.assertEqual(self.batch1.get_next_document_to_review(self.user1), None)

        # mark annotation as invalid
        self.annotation1.has_qa_invalidated = True
        self.annotation1.save()

        self.assertEqual(self.batch1.get_next_document_to_review(self.user1), self.doc1)

        # resubmit annotation
        self.annotation1.is_resubmitted = True
        self.annotation1.save()

        self.assertEqual(self.batch1.get_next_document_to_review(self.user1), None)
