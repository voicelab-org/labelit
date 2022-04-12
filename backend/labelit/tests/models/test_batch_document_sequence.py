from django.test import TestCase
from labelit.models import OrdinalTask, Project, OrdinalLabel, \
    SequenceBatch, Document, Dataset, BatchDocumentSequence, Annotation, \
    DocumentSequence
from django.db.models import signals
from django.contrib.auth import get_user_model
from labelit.signals.denormalizers.annotation_saved import annotation_saved
from labelit.signals.utils.temp_disconnect_signals import temp_disconnect_signal


signal_disconnect_kwargs = {
    'signal': signals.post_save,
    'receiver': annotation_saved,
    'sender': Annotation,
}


class BatchDocumentSequenceModelTests(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name="Feelin",
        )
        self.task1 = OrdinalTask.objects.create(
            name="Valence scale",
        )

        self.project.tasks.add(self.task1)
        self.dataset = Dataset.objects.create(
            name="IMDB"
        )
        self.document_sequence = DocumentSequence.objects.create(
            dataset=self.dataset,
            num_documents=2
        )
        self.doc1 = Document.objects.create(
            text="lovedit",
            dataset=self.dataset,
            document_sequence=self.document_sequence,
        )
        self.doc2 = Document.objects.create(
            text="hatedit",
            dataset=self.dataset,
            document_sequence=self.document_sequence,
        )
        self.batch1 = SequenceBatch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            project=self.project
        )
        self.batch1.sequences.add(self.document_sequence)
        self.batch1.save()
        self.batch_unit = self.batch1.get_batch_unit(self.doc1)
        self.user1 = get_user_model().objects.create(
            email="janedoe@labelit"
        )

        self.user2 = get_user_model().objects.create(
            email="juggernaut@labelit"
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

    def test_update_annotation_progress_statistics(self):
        self.assertEqual(
            self.batch_unit.num_done_annotators,
            0
        )
        self.batch_unit.update_annotation_progress_statistics(
            saved_annotation=self.annotation1
        )
        self.assertEqual(
            self.batch_unit.num_done_annotators,
            0
        ) # still 0, only one doc annotated
        self.assertEqual(
            self.batch_unit.num_annotators,
            1
        )
        with temp_disconnect_signal(**signal_disconnect_kwargs):
            self.annotation2 = Annotation.objects.create(
                annotator=self.user1,
                task=self.task1,
                document=self.doc2,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=False,
            )
        self.batch_unit.update_annotation_progress_statistics(
            saved_annotation=self.annotation2
        )
        self.assertEqual(
            self.batch_unit.num_done_annotators,
            0
        )
        with temp_disconnect_signal(**signal_disconnect_kwargs):
            self.annotation2.is_done = True
        self.annotation2.save()
        self.batch_unit.update_annotation_progress_statistics(
            saved_annotation=self.annotation2
        )
        self.assertEqual(
            self.batch_unit.num_done_annotators,
            1
        )

    def test_update_annotation_progress_statistics_with_two_tasks_and_two_annotators(self):
        task2 = OrdinalTask.objects.create(
            name="Arousal scale",
        )
        self.project.tasks.add(task2)
        self.batch_unit.update_annotation_progress_statistics(
            saved_annotation=self.annotation1
        )

        self.assertEqual(self.batch_unit.num_done_annotators, 0)

        self.assertEqual(
            self.batch_unit.num_annotators,
            1
        )
        with temp_disconnect_signal(**signal_disconnect_kwargs):
            self.annotation2 = Annotation.objects.create(
                annotator=self.user1,
                task=self.task1,
                document=self.doc2,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=True,
            )
            self.annotation3 = Annotation.objects.create(
                annotator=self.user1,
                task=task2,
                document=self.doc1,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=True,
            )
            self.annotation4 = Annotation.objects.create(
                annotator=self.user1,
                task=task2,
                document=self.doc2,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=True,
            )
        self.batch_unit.update_annotation_progress_statistics(
            saved_annotation=self.annotation2
        )
        self.assertEqual(
            self.batch_unit.num_done_annotators,
            1
        )
        with temp_disconnect_signal(**signal_disconnect_kwargs):
            self.annotation5 = Annotation.objects.create(
                annotator=self.user2,
                task=self.task1,
                document=self.doc1,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=True,
            )
            self.annotation6 = Annotation.objects.create(
                annotator=self.user2,
                task=self.task1,
                document=self.doc2,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=True,
            )
            self.annotation7 = Annotation.objects.create(
                annotator=self.user2,
                task=task2,
                document=self.doc1,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=True,
            )
            self.annotation8 = Annotation.objects.create(
                annotator=self.user2,
                task=task2,
                document=self.doc2,
                batch=self.batch1,
                project=self.batch1.project,
                is_done=False,
            )
        self.batch_unit.update_annotation_progress_statistics(
            saved_annotation=self.annotation2
        )
        self.assertEqual(
            self.batch_unit.num_done_annotators,
            1
        )
        self.assertEqual(
            self.batch_unit.num_annotators,
            2
        )
        with temp_disconnect_signal(**signal_disconnect_kwargs):
            self.annotation8.is_done = True
            self.annotation8.save()
        self.batch_unit.update_annotation_progress_statistics(
            saved_annotation=self.annotation2
        )
        self.assertEqual(
            self.batch_unit.num_done_annotators,
            2
        )


