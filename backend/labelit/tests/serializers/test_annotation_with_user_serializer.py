from django.contrib.auth import get_user_model
from django.test import TestCase

from labelit.models import (Annotation, Batch, Dataset, Document, OrdinalLabel,
                            OrdinalTask, Project)
from labelit.serializers import AnnotationWithUserSerializer


class AnnotationWithUserSerializerTests(TestCase):
    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="IMDB reviews",
        )
        self.docs = []

        for text in ["some text", "other text", "lorem ipsum", "doloris"]:
            self.docs.append(Document.objects.create(text=text, dataset=self.dataset))
        self.project = Project.objects.create(name="Sentiment")

        self.users = []

        for u in [
            ("jane", "doe", "janedoe@labelit"),
            ("john", "doe", "johndoe@labelit"),
            ("bat", "man", "batman@labelit"),
        ]:
            self.users.append(
                get_user_model().objects.create(
                    first_name=u[0], last_name=u[1], username=u[0] + u[1], email=u[2]
                )
            )

        self.batch = Batch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            project=self.project,
            num_documents=2,
        )
        self.batch.annotators.set(self.users)
        self.batch.documents.set(self.docs[:2])

        self.task = OrdinalTask.objects.create(
            name="Valence",
        )
        self.project.tasks.add(self.task)

        self.labels = []

        for index in range(0, 3):
            self.labels.append(
                OrdinalLabel.objects.create(
                    index=index,
                    task=self.task,
                )
            )

        self.annotation = Annotation.objects.create(
            annotator=self.users[0],
            batch=self.batch,
            document=self.docs[0],
            task=self.task,
            project=self.project,
        )
        self.annotation.labels.set([self.labels[1]])

        self.serializer1 = AnnotationWithUserSerializer(instance=self.annotation)

    def test_contains_expected_fields_and_specific_fields_and_resourcetype(self):
        self.assertEqual(
            set(self.serializer1.data.keys()),
            set(
                [
                    "annotator",
                    "batch",
                    "labels",
                    "document",
                    "task",
                    "project",
                    "document_sequence",
                    "is_done",
                    "id",
                    "has_qa_validated",
                    "has_qa_invalidated",
                    "is_resubmitted",
                    "qa_invalidation_comment",
                    "time",
                ]
            ),
        )
