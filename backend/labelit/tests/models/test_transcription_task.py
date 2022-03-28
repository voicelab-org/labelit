from django.test import TestCase
from django.contrib.auth import get_user_model
from labelit.models import (
    TranscriptionTask,
    Project,
    Dataset,
    Document,
    Batch,
    Label,
    Annotation,
    TranscriptionLabel,
)
from django.core.exceptions import ValidationError
from users.models import User

class TranscriptionTaskModelTests(TestCase):
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
            num_annotators_per_document=1,
        )
        self.batch.annotators.set([self.u1,])
        self.batch.documents.set([self.doc1, self.doc2])

        self.task = TranscriptionTask.objects.create(
            name="Transcribe stuff",
        )
        self.project.tasks.add(self.task)

        self.label1 = TranscriptionLabel.objects.create(
            task=self.task,
            transcript="some forbidden characters #"
        )

    def test_validate(self):
        with self.assertRaises(ValidationError):
            self.task.validate_labels([self.label1], True)
