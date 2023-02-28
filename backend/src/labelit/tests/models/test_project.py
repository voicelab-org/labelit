from django.test import TestCase
from labelit.models import (
    Task,
    OrdinalTask,
    CategoricalTask,
    Project,
    Batch,
    Document,
    Dataset,
    Annotation,
)
from labelit.tests import TestSetup
import itertools


class ProjectModelTests(TestSetup, TestCase):
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
        self.annotation3 = Annotation.objects.create(
            annotator=self.user2,
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        self.ANNOTATION_MODES = self.batch1.ANNOTATION_MODES
        self.EVEN = self.batch1.EVEN
        self.ALL_YOU_CAN_ANNOTATE = self.batch1.ALL_YOU_CAN_ANNOTATE

    def test_get_num_batches(self):
        self.assertEqual(self.project.get_num_batches(), 2)
        self.batch2.delete()
        self.assertEqual(self.project.get_num_batches(), 1)

    def test_get_num_done_documents(self):
        self.assertEqual(self.project.get_num_done_documents(), 0)

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
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )

        self.assertEqual(self.project.get_num_done_documents(), 1)

        for user, task in itertools.product(
            *[[self.user1, self.user2], [self.task1, self.task2]]
        ):
            Annotation.objects.create(
                annotator=user,
                task=task,
                document=self.doc4,
                batch=self.batch2,
                project=self.project,
                is_done=True,
            )
        self.assertEqual(self.project.get_num_done_documents(), 2)

    def test_get_num_done_batches(self):
        self.assertEqual(self.project.get_num_done_batches(), 0)

        for user, task, doc in itertools.product(
            *[
                [self.user1, self.user2],
                [self.task1, self.task2],
                [self.doc4, self.doc5],
            ]
        ):
            Annotation.objects.create(
                annotator=user,
                task=task,
                document=doc,
                batch=self.batch2,
                project=self.project,
                is_done=True,
            )

        self.assertEqual(self.project.get_num_done_batches(), 1)
