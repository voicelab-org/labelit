from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate
from labelit.models import Project, CategoricalTask, OrdinalTask, \
 OrdinalLabel, Batch, Document, Dataset, Task, Label, Annotation
from labelit.views import TaskViewSet


class TaskViewSetTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='tester@labelit',
            password='tester',
            )
        self.request_factory = APIRequestFactory()

        self.project = Project.objects.create(
            name="Feelin"
        )
        self.dataset = Dataset.objects.create(
            name="IMDB"
        )
        self.batch = Batch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            num_annotators_per_document=2,
            num_documents=2,
            project=self.project
        )
        self.doc1 = Document.objects.create(dataset=self.dataset)
        self.doc2 = Document.objects.create(dataset=self.dataset)

        self.u1 = get_user_model().objects.create(email="jogndoe@labelit")
        self.u2 = get_user_model().objects.create(email="gfhod@labelit")
        self.batch.annotators.set([self.u1, self.u2])
        self.batch.documents.set([self.doc1, self.doc2])

        self.task = CategoricalTask.objects.create(
            name="CategorizeAnger",
        )
        self.project.tasks.add(self.task)
        self.l1 = Label.objects.create(
            name="angry",
            task=self.task
        )
        self.l2 = Label.objects.create(
            name="not-angry",
            task=self.task
        )

    def _authenticate(self, request):
        force_authenticate(request, user=self.user)

    def test_get_list_unauthenticated_returns_status_code_401(self):
        request = self.request_factory.get('')
        response = TaskViewSet.as_view(
            actions={'get': 'list'}
        )(request)
        self.assertEqual(response.status_code, 401)

    def test_get_list_authenticated_returns_status_code_200(self):
        request = self.request_factory.get('')
        self._authenticate(request)
        response = TaskViewSet.as_view(
            actions={'get': 'list'}
        )(request)
        self.assertEqual(response.status_code, 200)

    """
    def test_get_list_returns_task_generic_fields_and_specific_fields_and_resourcetype(self):
        request = self.request_factory.get('')
        self._authenticate(request)
        response = TaskViewSet.as_view(
            actions={'get': 'list'}
        )(request)

        for item in response.data:
            for generic_field in [
                'name',
                'project',
                'can_documents_be_invalidated'
            ]:
                self.assertTrue(generic_field in item.keys())
            if item['name'] == "Five emotions":
                self.assertTrue('are_categories_exclusive' in item.keys())
            self.assertTrue('resourcetype' in item.keys())
    """

    def test_get_a_task_returns_task_with_nested_labels(self):
        request = self.request_factory.get('')
        self._authenticate(request)
        response = TaskViewSet.as_view(
            actions={'get': 'retrieve'}
        )(request, pk=self.task.pk)
        self.assertEqual(
            len(response.data['labels']),
            2
        )
        self.assertEqual(
            response.data['labels'][0]['resourcetype'],
            'Label'
        )

    def test_get_agreement_stats_for_batch(self):

        a1 = Annotation.objects.create(
            annotator=self.u1,
            document=self.doc1,
            task=self.task,
            batch=self.batch,
            project=self.project,
            is_done=True
        )
        a1.labels.add(self.l1)
        a1.save()
        
        a2 = Annotation.objects.create(
            annotator=self.u1,
            document=self.doc2,
            task=self.task,
            batch=self.batch,
            project=self.project,
            is_done=True
        )
        a2.labels.add(self.l1)
        a2.save()

        a3 = Annotation.objects.create(
            annotator=self.u2,
            document=self.doc1,
            task=self.task,
            batch=self.batch,
            project=self.project,
            is_done=True
        )
        a3.labels.add(self.l2)
        a3.save()

        a4 = Annotation.objects.create(
            annotator=self.u2,
            document=self.doc2,
            task=self.task,
            batch=self.batch,
            project=self.project,
            is_done=True
        )
        a4.labels.add(self.l1)
        a4.save()

        request = self.request_factory.get(
            '',
            {
                'batch_id': self.batch.pk
            }
        )
        self._authenticate(request)
        response = TaskViewSet.as_view(
            actions={'get': 'get_agreement_stats_for_batch'}
        )(request, pk=self.task.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "metric" in response.data
        )
