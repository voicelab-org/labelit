from django.test import TestCase
from django.contrib.auth import get_user_model
from labelit.models import CategoricalTask, Project, \
    Dataset, Document, Batch, Label, Annotation
from django.http import Http404
from labelit.tests import TestSetup
from users.models import User


class CategoricalTaskModelTests(TestSetup, TestCase):
    fixtures = ['test_data']

    def setUp(self):
        self.project = Project.objects.get(pk=6)
        self.u1 = User.objects.all().first()
        self.u2 = User.objects.all()[1]

        self.dataset = Dataset.objects.get(pk=3)
        self.doc1 = Document.objects.get(pk=6)
        self.doc2 = Document.objects.get(pk=7)
        self.batch = Batch.objects.create(
            dataset=self.dataset,
            name="Batch 1",
            project=self.project,
            num_annotators_per_document=2
        )
        self.batch.annotators.set([self.u1, self.u2])
        self.batch.documents.set([self.doc1, self.doc2])

        self.task = CategoricalTask.objects.create(
            name="CategorizeAnger",
            are_categories_exclusive=True,
        )
        self.project.tasks.add(self.task)
        self.label1 = Label.objects.create(
            name="anger",
            task=self.task
        )
        self.label2 = Label.objects.create(
            name="not-anger",
            task=self.task
        )

    def test_agreement_stats(self):
        self.a1 = Annotation.objects.create(
            annotator=self.u1,
            task=self.task,
            batch=self.batch,
            document=self.doc1,
            project=self.project,
        )
        self.a1.labels.set([self.label1])
        self.a1.is_done = True
        self.a1.save()

        # no agreement returned with no doc fully annotated
        with self.assertRaises(Http404):
            self.task.get_agreement_stats(self.batch)

        self.a2 = Annotation.objects.create(
            annotator=self.u2,
            task=self.task,
            batch=self.batch,
            document=self.doc1,
            project=self.project,
        )
        self.a2.labels.set([self.label1])
        self.a2.is_done = True
        self.a2.save()

        # no agreement returned with only one doc annotated
        with self.assertRaises(Http404):
            self.task.get_agreement_stats(self.batch)

        self.a3 = Annotation.objects.create(
            annotator=self.u1,
            task=self.task,
            batch=self.batch,
            document=self.doc2,
            project=self.project,
        )
        self.a3.labels.set([self.label1])
        self.a3.is_done = True
        self.a3.save()

        self.a4 = Annotation.objects.create(
            annotator=self.u2,
            task=self.task,
            batch=self.batch,
            document=self.doc2,
            project=self.project,
        )
        self.a4.labels.set([self.label2])
        self.a4.is_done = True
        self.a4.save()

        agreement_stats = self.task.get_agreement_stats(self.batch)
        self.assertTrue(
            agreement_stats["value"] <= 1.0
        )
        self.assertTrue(
            agreement_stats["value"] >= -1.0
        )



