from labelit.models import (
    Task,
    OrdinalTask,
    CategoricalTask,
    Project,
    Batch,
    Document,
    Dataset,
    Annotation
)

from users.models import User

class TestSetup():
    fixtures = ['test_data']

    def setUp(self):
        self.dataset = Dataset.objects.get(pk=3)
        self.project = Project.objects.get(pk=6)
        self.batch1 = Batch.objects.get(pk=10)
        self.doc1 = Document.objects.get(pk=6)
        self.doc2 = Document.objects.get(pk=7)
        self.doc3 = Document.objects.get(pk=8)

        self.batch2 = Batch.objects.get(pk=11)
        self.doc4 = Document.objects.get(pk=9)
        self.doc5 = Document.objects.get(pk=10)

        self.user1 = User.objects.all().first()
        self.user2 = User.objects.all()[1]

        self.task1 = Task.objects.get(pk=8)
        self.task2 = Task.objects.get(pk=9)
