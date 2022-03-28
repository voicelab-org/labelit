from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate
from labelit.models import Project, CategoricalTask, OrdinalTask, \
 OrdinalLabel, Dataset, Batch, Document, Dataset
from labelit.views import DatasetViewSet


class DatasetViewSetTests(TestCase):

    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.annotator1 = get_user_model().objects.create(
            email='tester@labelit',
            password='tester',
            is_staff=True
        )
        self.dataset = Dataset.objects.create(name="IMDB")

    def _authenticate(self, request):
        force_authenticate(request, user=self.annotator1)

    def test_get_list_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get('')
        response = DatasetViewSet.as_view(
            actions={'get': 'list'}
        )(request)
        self.assertEqual(response.status_code, 401)

    def test_get_list_authenticated_returns_status_code_200(self):
        request = self.request_factory.get('')
        self._authenticate(request)
        response = DatasetViewSet.as_view(
            actions={'get': 'list'}
        )(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.data),
            1
        )
