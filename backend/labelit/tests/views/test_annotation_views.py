from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate
from labelit.models import Project, CategoricalTask, OrdinalTask, \
 OrdinalLabel, Dataset, Batch, Document, Annotation
from labelit.views import AnnotationViewSet
from django.db.models import signals
from labelit.signals.denormalizers.annotation_saved import annotation_saved


signal_disconnect_kwargs = {
    'signal': signals.post_save,
    'receiver': annotation_saved,
    'sender': Annotation,
}


class AnnotationViewSetTests(TestCase):

    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.annotator1 = get_user_model().objects.create(
            email='tester@labelit',
            password='tester',
        )
        self.project = Project.objects.create(
            name="Feelin"
        )
        self.task1 = OrdinalTask.objects.create(
            name="Valence scale",
        )
        self.project.tasks.add(self.task1)
        self.label1 = OrdinalLabel.objects.create(
            index=0,
            task=self.task1
        )
        self.label2 = OrdinalLabel.objects.create(
            index=1,
            task=self.task1
        )
        self.task2 = CategoricalTask.objects.create(
            name="Five emotions",
        )
        self.project.tasks.add(self.task2)
        self.dataset = Dataset.objects.create(name="IMDB")
        self.batch = Batch.objects.create(
            name='Batch 1',
            dataset=self.dataset,
            project=self.project
        )
        self.document = Document.objects.create(
            text="lovediit",
            dataset=self.dataset
        )
        self.batch.documents.add(self.document)

    def _authenticate(self, request):
        force_authenticate(request, user=self.annotator1)

    def test_get_list_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get('')
        response = AnnotationViewSet.as_view(
            actions={'get': 'list'}
        )(request)
        self.assertEqual(response.status_code, 401)

    def test_get_list_authenticated_returns_status_code_200(self):
        request = self.request_factory.get('')
        self._authenticate(request)
        response = AnnotationViewSet.as_view(
            actions={'get': 'list'}
        )(request)
        self.assertEqual(response.status_code, 200)

    def test_create_annotation_for_ordinal_task_with_valid_label_returns_201(self):
        request = self.request_factory.post(
            '',
            data={
                'annotator': self.annotator1.pk,
                'task': self.task1.pk,
                'batch': self.batch.pk,
                'labels': [self.label1.pk],
                'document': self.document.pk,
                'project': self.project.pk,
            }
        )
        self._authenticate(request)
        # with temp_disconnect_signal(**signal_disconnect_kwargs):
        response = AnnotationViewSet.as_view(
            actions={'post': 'create'}
        )(request)
        self.assertEqual(response.status_code, 201)

    def test_create_annotation_for_ordinal_task_with_two_label_returns_400(self):
        request = self.request_factory.post(
            '',
            data={
                'annotator': self.annotator1.pk,
                'task': self.task1.pk,
                'batch': self.batch.pk,
                'labels': [self.label1.pk, self.label2.pk],
                'document': self.document.pk,
                'project': self.project.pk,
            }
        )
        self._authenticate(request)
        # with temp_disconnect_signal(**signal_disconnect_kwargs):
        response = AnnotationViewSet.as_view(
            actions={'post': 'create'}
        )(request)
        self.assertEqual(response.status_code, 400)

    def test_update_annotation_for_ordinal_task_with_valid_label_returns_200(self):
        # first create annotation
        request = self.request_factory.post(
            '',
            data={
                'annotator': self.annotator1.pk,
                'task': self.task1.pk,
                'batch': self.batch.pk,
                'labels': [self.label1.pk],
                'document': self.document.pk,
                'project': self.project.pk,
            }
        )
        self._authenticate(request)
        # with temp_disconnect_signal(**signal_disconnect_kwargs):
        response = AnnotationViewSet.as_view(
            actions={'post': 'create'}
        )(request)
        self.assertEqual(response.status_code, 201)
        id = response.data['id']
        request = self.request_factory.post(
            '',
            data={
                'id': id,
                'annotator': self.annotator1.pk,
                'task': self.task1.pk,
                'batch': self.batch.pk,
                'labels': [self.label2.pk],
                'document': self.document.pk,
                'project': self.project.pk,
            }
        )
        self._authenticate(request)
        # with temp_disconnect_signal(**signal_disconnect_kwargs):
        response = AnnotationViewSet.as_view(
            actions={'post': 'update'}
        )(request, pk=id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], id)