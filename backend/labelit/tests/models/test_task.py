from django.test import TestCase
from labelit.models import Task, CategoricalTask, OrdinalTask, \
    Project


class PolymorphicTaskModelTests(TestCase):
    fixtures = ['test_data']


    def setUp(self):
        self.project = Project.objects.create(
            name="Feelin",
        )
        t1 = CategoricalTask.objects.create(
            name="Big five emotions",
        )
        t2 = OrdinalTask.objects.create(
            name="Valence scale",
        )
        self.project.tasks.set([t1, t2])

    def test_query_polymorphic_task_retrieves_specific_task_models(self):
        all_tasks = Task.objects.filter(projects=self.project)
        self.assertEqual(
            all_tasks.count(),
            2
        )
        for cls in [CategoricalTask, OrdinalTask]:
            self.assertTrue(
                cls in [
                    o.__class__
                    for o in all_tasks
                ]
            )
