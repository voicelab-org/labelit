import copy
from django.test import TestCase
from labelit.models import Project, Label, OrdinalTask, OrdinalLabel
from labelit.serializers import TaskSerializer
from collections import OrderedDict


class TaskSerializerTests(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name="Feelin",
        )
        self.task1 = OrdinalTask.objects.create(
            name='Valence',
        )
        self.project.tasks.add(self.task1)
        self.label0 = OrdinalLabel.objects.create(
            task=self.task1,
            index=0
        )
        self.label1 = OrdinalLabel.objects.create(
            task=self.task1,
            index=1
        )

        self.serializer1 = TaskSerializer(
            instance=self.task1
        )

    def test_contains_expected_fields(self):
        data = self.serializer1.data
        self.assertEqual(
            set(data.keys()),
            set([
                'id',
                'name',
                'projects',
                'can_documents_be_invalidated',
                'labels',
                'html_guidelines'
            ])
        )

    def test_contains_nested_labels(self):
        labels = self.serializer1.data['labels']
        self.assertTrue(type(labels) == list)
        self.assertTrue(type(labels[0]) == OrderedDict)
        self.assertEqual(len(labels), 2)