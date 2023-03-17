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
)
from labelit.views import StatsView
from labelit.tests import TestSetup


class StatsViewTests(TestSetup, TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()

        self.user = get_user_model().objects.create(
            email="tester@labelit",
            password="tester",
        )
        Annotation.objects.all().delete()
        super().setUp()

    def _authenticate(self, request):
        force_authenticate(request, user=self.user)

    def test_view_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get("")
        response = StatsView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_view_returns_correct_data(self):
        request = self.request_factory.get("")
        self._authenticate(request)
        response = StatsView.as_view()(request)
        self.assertEqual(response.data["num_docs"], 0)
        self.assertEqual(response.data["stats_per_annotator"], [])
        self.assertEqual(response.data["stats_per_annotator_per_day"], [])
        self.assertTrue("total_duration" in response.data.keys())

        Annotation.objects.create(
            annotator=self.batch1_annotators[0],
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        Annotation.objects.create(
            annotator=self.batch1_annotators[0],
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        Annotation.objects.create(
            annotator=self.batch1_annotators[1],
            task=self.task1,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        request = self.request_factory.get("")
        self._authenticate(request)
        response = StatsView.as_view()(request)
        self.assertEqual(response.data["num_docs"], 1)
        Annotation.objects.create(
            annotator=self.batch1_annotators[1],
            task=self.task2,
            document=self.doc1,
            batch=self.batch1,
            project=self.batch1.project,
            is_done=True,
        )
        request = self.request_factory.get("")
        self._authenticate(request)
        response = StatsView.as_view()(request)
        self.assertEqual(response.data["num_docs"], 2)  # failing here, num_docs is 0