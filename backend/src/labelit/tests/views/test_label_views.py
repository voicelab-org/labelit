from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate
from labelit.models import Project, OrdinalTask, OrdinalLabel, Label
from labelit.views import LabelViewSet


class LabelViewSetTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="tester@labelit",
            password="tester",
        )
        self.request_factory = APIRequestFactory()

        self.project = Project.objects.create(
            name="Feelin", target_deadline="2023-03-08", target_num_documents=100
        )
        self.task = OrdinalTask.objects.create(
            name="Valence scale",
        )
        self.project.tasks.add(self.task)
        self.label1 = OrdinalLabel.objects.create(task=self.task, index=0)

    def _authenticate(self, request):
        force_authenticate(request, user=self.user)

    def test_get_list_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get("")
        response = LabelViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 401)

    def test_get_list_authenticated_returns_status_code_200(self):
        request = self.request_factory.get("")
        self._authenticate(request)
        response = LabelViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 200)

    def test_create_label_successful(self):
        request = self.request_factory.post(
            "", data={"index": 1, "task": self.task.pk, "resourcetype": "OrdinalLabel"}
        )
        self._authenticate(request)
        response = LabelViewSet.as_view(actions={"post": "create"})(request)
        self.assertEqual(response.status_code, 201)
        labels = Label.objects.all()
        self.assertEqual(labels.count(), 2)

    def test_create_ordinal_label_with_duplicate_index_returns_400_Bad_Request(self):
        request = self.request_factory.post(
            "",
            data={
                "index": 0,  # duplicate index
                "task": self.task.pk,
                "resourcetype": "OrdinalLabel",
            },
        )
        self._authenticate(request)
        response = LabelViewSet.as_view(actions={"post": "create"})(request)
        self.assertEqual(response.status_code, 400)
        labels = Label.objects.all()
        self.assertEqual(labels.count(), 1)
