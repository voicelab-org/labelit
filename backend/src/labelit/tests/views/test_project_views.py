from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate
from labelit.models import Project, Dataset, Batch, Document
from labelit.views import ProjectViewSet
from labelit.tests import TestSetup


class ProjectViewSetTests(TestSetup, TestCase,):
    def setUp(self):

        super().setUp()
        self.user = get_user_model().objects.create(
            email="tester@labelit",
            password="tester",
        )
        self.request_factory = APIRequestFactory()
        self.project = Project.objects.create(
            name="Feelin", target_deadline="2023-03-08", target_num_documents=100
        )

    def _authenticate(self, request):
        force_authenticate(request, user=self.user)

    def test_get_list_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get("")
        response = ProjectViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 401)

    def test_get_list_authenticated_returns_status_code_200(self):
        request = self.request_factory.get("")
        self._authenticate(request)
        response = ProjectViewSet.as_view(actions={"get": "list"})(request)
        self.assertEqual(response.status_code, 200)

    def test_create_project_successful(self):
        request = self.request_factory.post("", data={
            "name": "Transcribing meetings",
            "is_audio_annotated": True,
            "is_text_annotated": False,
            "enable_region_annotation": False,
            "are_sequenced_annotated": False,
            'tasks': [self.task1.pk],
            "time_inactivity_threshold": 5000,
            "do_display_timer_time": False,
            "does_audio_playing_count_as_activity": True,
            "target_deadline": "2022-01-03",
            "target_num_documents": 100,
            "description": "This project consists in transcribing real-life meetings"
        })
        self._authenticate(request)
        response = ProjectViewSet.as_view(actions={"post": "create"})(request)
        self.assertEqual(response.status_code, 201)
        projects = Project.objects.all()
        self.assertEqual(projects.count(), 3)

    def test_get_remaining_units_in_dataset(self):
        dataset = Dataset.objects.create(name="IMDB")
        document = Document.objects.create(dataset=dataset, text="love the movie!")
        request = self.request_factory.get("", {"dataset_id": dataset.pk})
        self._authenticate(request)
        response = ProjectViewSet.as_view(
            actions={"get": "get_remaining_units_in_dataset"}
        )(request, pk=self.project.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
