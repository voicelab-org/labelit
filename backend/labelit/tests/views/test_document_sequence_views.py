from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate
from labelit.models import (
    Project,
    CategoricalTask,
    OrdinalTask,
    OrdinalLabel,
    Batch,
    Document,
    Dataset,
    Task,
    Label,
    Annotation,
    SequenceBatch,
    DocumentSequence,
)
from labelit.views import DocumentSequenceViewSet


class TaskViewSetTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="tester@labelit",
            password="tester",
        )
        self.request_factory = APIRequestFactory()

        self.project = Project.objects.create(name="Feelin")
        self.dataset = Dataset.objects.create(name="IMDB")

        self.seq_batch = SequenceBatch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            num_annotators_per_document=2,
            num_documents=2,
            project=self.project,
        )

        self.doc_seq = DocumentSequence.objects.create(
            dataset=self.dataset, num_documents=2
        )
        self.doc1 = Document.objects.create(
            dataset=self.dataset,
            document_sequence=self.doc_seq,
            sequence_index=0,
        )
        self.doc2 = Document.objects.create(
            dataset=self.dataset,
            document_sequence=self.doc_seq,
            sequence_index=0,
        )

    def _authenticate(self, request):
        force_authenticate(request, user=self.user)

    def test_get_list_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get("")
        response = DocumentSequenceViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 401)

    def test_get_list_authenticated_returns_status_code_200(self):
        request = self.request_factory.get("")
        self._authenticate(request)
        response = DocumentSequenceViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 200)
