from django.test import TestCase
from labelit.models import Document, Dataset, DocumentSequence
from labelit.serializers import DocumentSequenceSerializer


class DocumentSequenceSerializerTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="IMDB reviews"
        )
        self.document_sequence = DocumentSequence.objects.create(
            dataset=self.dataset,
            num_documents=2
        )
        self.document1 = Document.objects.create(
            text="The movie was so wishy-washy I could do my laundry with it",
            dataset=self.dataset,
            document_sequence=self.document_sequence,
            sequence_index=0,
        )
        self.document2 = Document.objects.create(
            text="If my island had a TV, I would bring that one movie with me",
            dataset=self.dataset,
            document_sequence=self.document_sequence,
            sequence_index=1,
        )
        self.serializer = DocumentSequenceSerializer(
            instance=self.document_sequence
        )

    def test_contains_expected_fields_and_specific_fields_and_resourcetype(self):
        self.assertEqual(
            set(self.serializer.data.keys()),
            set([
                'dataset',
                'num_documents'
            ])
        )
