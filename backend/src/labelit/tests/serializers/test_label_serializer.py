from django.test import TestCase
from labelit.models import OrdinalTask, Project, OrdinalLabel
from labelit.serializers import LabelPolymorphicSerializer


class LabelSerializerTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Feelin",
            target_deadline="2023-03-08",
            target_num_documents=100,
        )
        self.task1 = OrdinalTask.objects.create(
            name="Valence",
        )
        self.project.tasks.add(self.task1)
        self.ord_0 = OrdinalLabel.objects.create(task=self.task1, index=0)
        self.ord_1 = OrdinalLabel.objects.create(task=self.task1, index=1)
        self.ord_2 = OrdinalLabel.objects.create(task=self.task1, index=2)
        self.serializer1 = LabelPolymorphicSerializer(instance=self.ord_1)

    def test_contains_expected_fields_and_specific_fields_and_resourcetype(self):
        data = self.serializer1.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "task", "name", "color", "index", "resourcetype"]),
        )
