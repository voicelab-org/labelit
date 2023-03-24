from django.test import TestCase
from django.contrib.auth import get_user_model

from labelit.utils.agreement_metrics.ordinal_alpha import OrdinalAlphaMetric
from labelit.models import (
    Project,
    Dataset,
    Document,
    Batch,
    OrdinalTask,
    OrdinalLabel,
    Annotation,
)
from users.models import User


class OrdinalAlphaTests(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.project = Project.objects.get(pk=6)

        self.u1 = User.objects.all().first()
        self.u2 = User.objects.all()[1]
        self.dataset = Dataset.objects.get(pk=3)
        self.doc1 = Document.objects.get(pk=6)
        self.doc2 = Document.objects.get(pk=7)
        self.doc3 = Document.objects.get(pk=8)
        self.batch = Batch.objects.create(
            dataset=self.dataset,
            name="Batch 1",
            project=self.project,
            num_annotators_per_document=2,
        )
        self.batch.annotators.set([self.u1, self.u2])
        self.batch.documents.set([self.doc1, self.doc2, self.doc3])

        self.task = OrdinalTask.objects.create(
            name="Arousal",
        )
        self.project.tasks.add(self.task)
        self.label1 = OrdinalLabel.objects.create(index=0, task=self.task)
        self.label2 = OrdinalLabel.objects.create(index=1, task=self.task)
        self.label3 = OrdinalLabel.objects.create(index=2, task=self.task)
        self.a1 = Annotation.objects.create(
            is_done=True,
            annotator=self.u1,
            task=self.task,
            batch=self.batch,
            document=self.doc1,
            project=self.project,
        )
        self.a1.labels.set([self.label1])
        self.a1.save()

        self.a2 = Annotation.objects.create(
            is_done=True,
            annotator=self.u2,
            task=self.task,
            batch=self.batch,
            document=self.doc1,
            project=self.project,
        )
        self.a2.labels.set([self.label1])
        self.a2.save()

        self.a3 = Annotation.objects.create(
            is_done=True,
            annotator=self.u1,
            task=self.task,
            batch=self.batch,
            document=self.doc2,
            project=self.project,
        )
        self.a3.labels.set([self.label1])
        self.a3.save()

        self.a4 = Annotation.objects.create(
            is_done=True,
            annotator=self.u2,
            task=self.task,
            batch=self.batch,
            document=self.doc2,
            project=self.project,
        )
        self.a4.labels.set([self.label2])
        self.a4.save()
        self.metric = OrdinalAlphaMetric(num_labels=3)

    def test_format_labelit_ordinal_annotations(self):
        formatted = self.metric.format_annotations_queryset(Annotation.objects.all())
        """
            def format_annotations_queryset(self, annotations):
                Returns a list of tuples (annotator_id, document_id, label value).
        """
        self.assertEqual(
            set(formatted),
            {
                (self.u1.pk, self.doc1.pk, self.label1.pk),
                (self.u1.pk, self.doc2.pk, self.label1.pk),
                (self.u2.pk, self.doc1.pk, self.label1.pk),
                (self.u2.pk, self.doc2.pk, self.label2.pk),
            },
        )

    def test_ordinal_distance(self):
        num_labels = 3
        self.assertEqual(self.metric.ordinal_distance(0, 2), 1.0)
        self.assertEqual(self.metric.ordinal_distance(0, 1), 0.5)

    def test_ordinal_krippendorff_alpha(self):
        def _alpha():
            return self.metric.ordinal_krippendorff_alpha(
                data=self.metric.format_annotations_queryset(Annotation.objects.all()),
            )

        alpha = _alpha()
        self.assertTrue(alpha <= 1.0)
        self.assertEqual(alpha, 0.0)

        self.a4.labels.set([self.label1])
        alpha = _alpha()

        self.assertEqual(alpha, 1.0)

        a5 = Annotation.objects.create(
            is_done=True,
            document=self.doc3,
            annotator=self.u1,
            project=self.project,
            batch=self.batch,
            task=self.task,
        )
        a5.labels.set([self.label3])
        a5.save()

        a6 = Annotation.objects.create(
            is_done=True,
            document=self.doc3,
            annotator=self.u2,
            project=self.project,
            batch=self.batch,
            task=self.task,
        )
        a6.labels.set([self.label3])
        a6.save()

        self.assertEqual(_alpha(), 1.0)

        a6.labels.set([self.label2])
        a6.save()

        self.assertEqual(round(_alpha(), 3), 0.615)

        a6.labels.set([self.label1])
        a6.save()
        self.assertEqual(_alpha(), 0.0)
