from django.test import TestCase
from django.contrib.auth import get_user_model
from labelit.models import (
    LiveCorrectTask,
    Project,
    Dataset,
    Document,
    Batch,
    LiveCorrectLabel,
    TimedTranscript,
    TimedTranscriptSegment,
)
from django.core.exceptions import ValidationError
from users.models import User

class LiveCorrectTaskModelTests(TestCase):
    fixtures = ['test_data']

    def setUp(self):
        self.project = Project.objects.get(pk=6)

        self.u1 = User.objects.all().first()
        self.u2 = User.objects.all()[1]
        self.dataset = Dataset.objects.get(pk=3)
        self.doc1 = Document.objects.get(pk=6)
        self.batch = Batch.objects.create(
            dataset=self.dataset,
            name="Batch 1",
            project=self.project,
            num_annotators_per_document=1,
        )
        self.batch.annotators.set([self.u1,])
        self.batch.documents.set([self.doc1,])
        self.timed_transcript = TimedTranscript.objects.create()
        self.timed_transcript_segment_1 = TimedTranscriptSegment.objects.create(
            timed_transcript=self.timed_transcript,
            transcript="Hello my name is Andy",
            start_time=0.0,
        )
        self.timed_transcript_segment_2 = TimedTranscriptSegment.objects.create(
            timed_transcript=self.timed_transcript,
            transcript="and I live in San Francisco",
            start_time=3.2,
        )

        self.task = LiveCorrectTask.objects.create(
            name="Live correct some transcription",
        )
        self.project.tasks.add(self.task)

        self.label1 = LiveCorrectLabel.objects.create(
            task=self.task,
            transcript="Hello my name is Annie #",
            timed_transcript_segment=self.timed_transcript_segment_1,
        )
        self.label2 = LiveCorrectLabel.objects.create(
            task=self.task,
            transcript="and I live in San Francisco",
            timed_transcript_segment=self.timed_transcript_segment_2,
        )

    def test_validate(self):
        with self.assertRaises(ValidationError):
            self.task.validate_labels([self.label1, self.label2], True)
        self.task.validate_labels([self.label2], True)