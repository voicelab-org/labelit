from django.test import TestCase
from labelit.models import Document, Dataset
from labelit.serializers import DocumentSerializer


class DocumentSerializerTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="IMDB reviews"
        )
        self.document = Document.objects.create(
            text="The movie was so wishy-washy I could do my laundry with it",
            dataset=self.dataset
        )
        self.serializer = DocumentSerializer(
            instance=self.document
        )

    def test_contains_expected_fields_and_specific_fields_and_resourcetype(self):
        self.assertEqual(
            set(self.serializer.data.keys()),
            set([
                'id',
                'text',
                'audio_filename',
                'dataset',
                'document_sequence',
                'sequence_index',
                'timed_transcript',
            ])
        )
