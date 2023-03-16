from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate
from labelit.models import Project, Batch, SequenceBatch, Dataset, Document, OrdinalTask
from labelit.views import BatchViewSet


class BatchViewSetTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="tester@labelit",
            password="tester",
        )
        self.user2 = get_user_model().objects.create(
            email="janedoe", password="janedoe"
        )
        self.request_factory = APIRequestFactory()
        self.project = Project.objects.create(
            name="Feelin", target_deadline="2023-03-08", target_num_documents=100
        )
        self.task1 = OrdinalTask.objects.create(
            name="Valence",
        )
        self.task2 = OrdinalTask.objects.create(
            name="Arousal",
        )
        self.project.tasks.set([self.task1, self.task2])
        self.dataset = Dataset.objects.create(name="IMDB")
        self.doc1 = Document.objects.create(text="lovedit", dataset=self.dataset)
        self.batch = Batch.objects.create(
            name="Batch1",
            dataset=self.dataset,
            project=self.project,
        )
        self.batch.annotators.set([self.user, self.user2])
        self.batch.documents.add(self.doc1)
        self.project2 = Project.objects.create(
            name="Scriber", target_deadline="2023-03-08", target_num_documents=100
        )
        self.batch2 = SequenceBatch.objects.create(
            name="Batch2", dataset=self.dataset, project=self.project2
        )
        self.batch3 = Batch.objects.create(
            name="Batch3",
            dataset=self.dataset,
            project=self.project,
        )

    def _authenticate(self, request):
        force_authenticate(request, user=self.user)

    def test_get_list_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get("")
        response = BatchViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 401)

    def test_get_list_authenticated_returns_status_code_200(self):
        request = self.request_factory.get("")
        self._authenticate(request)
        response = BatchViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 200)

    def test_get_batches_in_a_project(self):
        request = self.request_factory.get(
            "",
            {"project_id": self.project.pk},
        )
        self._authenticate(request)
        response = BatchViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_one_batch(self):
        request = self.request_factory.get(
            "",
        )
        self._authenticate(request)
        response = BatchViewSet.as_view(actions={"get": "retrieve"})(
            request, pk=self.batch.pk
        )
        self.assertEqual(response.status_code, 200)

    def test_get_progress(self):
        request = self.request_factory.get(
            "",
        )
        self._authenticate(request)
        response = BatchViewSet.as_view(actions={"get": "get_progress"})(
            request, pk=self.batch.pk
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["num_done_units"], 0)
        self.assertEqual(response.data["total"], 1)

    def test_get_progress_for_sequence_batch(self):
        self.request_factory = APIRequestFactory()
        request = self.request_factory.get(
            "",
        )
        self._authenticate(request)
        response = BatchViewSet.as_view(actions={"get": "get_progress"})(
            request, pk=self.batch2.pk
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["num_done_units"], 0)
        self.assertEqual(response.data["total"], 1)

    def test_get_next_document_to_annotate(self):
        request = self.request_factory.get(
            "",
        )
        self._authenticate(request)
        response = BatchViewSet.as_view(
            actions={"get": "get_next_document_to_annotate"}
        )(request, pk=self.batch.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("document" in response.data.keys())
        self.assertTrue("annotations" in response.data.keys())
        self.assertEqual(
            len(response.data["annotations"]), self.project.tasks.all().count()
        )
