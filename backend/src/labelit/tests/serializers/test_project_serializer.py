from django.test import TestCase
from labelit.models import Task, CategoricalTask, OrdinalTask, Project
from labelit.serializers import ProjectSerializer


class ProjectSerializerTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Feelin",
        )
        self.task1 = OrdinalTask.objects.create(
            name="Valence",
        )
        self.task2 = CategoricalTask.objects.create(
            name="Valence", are_categories_exclusive=False
        )
        self.project.tasks.set([self.task1, self.task2])
        self.serializer1 = ProjectSerializer(instance=self.project)

    def test_contains_expected_fields(self):
        data = self.serializer1.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "name",
                    "is_audio_annotated",
                    "is_text_annotated",
                    "are_sequences_annotated",
                    "tasks",
                    "timer_inactivity_threshold",
                ]
            ),
        )
