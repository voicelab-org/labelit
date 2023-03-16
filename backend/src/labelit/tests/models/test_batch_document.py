from django.test import TestCase
from django.contrib.auth import get_user_model
from labelit.models import (
    OrdinalTask,
    Project,
    OrdinalLabel,
    Batch,
    Document,
    Dataset,
    BatchDocument,
    Annotation,
)
from django.db.models import signals
from labelit.signals.denormalizers.annotation_saved import annotation_saved
from labelit.signals.utils.temp_disconnect_signals import temp_disconnect_signal


signal_disconnect_kwargs = {
    "signal": signals.post_save,
    "receiver": annotation_saved,
    "sender": Annotation,
}


from labelit.tests import TestSetup


class BatchDocumentModelTests(TestSetup, TestCase):
    def setUp(self):
        super().setUp()
        """
        self.project = Project.objects.create(
            name="Feelin",
        )
        self.task1 = OrdinalTask.objects.create(
            name="Valence scale",
            project=self.project
        )
        self.dataset = Dataset.objects.create(
            name="IMDB"
        )
        self.doc1 = Document.objects.create(
            text="lovedit",
            dataset=self.dataset
        )
        self.batch1 = Batch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            project=self.project
        )
        self.batch1.documents.add(self.doc1)
        """
        self.batch_document = BatchDocument.objects.get(
            batch=self.batch1, document=self.doc1
        )

        with temp_disconnect_signal(**signal_disconnect_kwargs):
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
                task=self.task2,
                document=self.doc1,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=True,
            )

    def test_update_annotation_progress_statistics(self):
        self.assertEqual(self.batch_document.num_done_annotators, 0)
        self.assertEqual(self.batch_document.num_annotators, 0)
        self.batch_document.update_annotation_progress_statistics(
            saved_annotation=self.annotation1
        )
        self.assertEqual(self.batch_document.num_done_annotators, 1)
        self.assertEqual(self.batch_document.num_annotators, 1)

    def test_update_annotation_progress_statistics_with_two_annotators(self):
        self.batch_document.update_annotation_progress_statistics(
            saved_annotation=self.annotation1
        )
        self.assertEqual(self.batch_document.num_done_annotators, 1)
        self.assertEqual(self.batch_document.num_annotators, 1)
        with temp_disconnect_signal(**signal_disconnect_kwargs):
            self.annotation3 = Annotation.objects.create(
                annotator=self.user2,
                task=self.task1,
                document=self.doc1,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=False,
            )
            self.annotation3 = Annotation.objects.create(
                annotator=self.user2,
                task=self.task2,
                document=self.doc1,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=False,
            )
        self.batch_document.update_annotation_progress_statistics(
            saved_annotation=self.annotation2
        )
        self.assertEqual(self.batch_document.num_annotators, 2)
