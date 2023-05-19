from django.test import TestCase
from labelit.models import (
    Project,
    Dataset,
    Document,
    Batch,
    SortedSampler,
)
from users.models import User


class SortedSamplerTests(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.project = Project.objects.get(pk=6)

        self.sorted_sampler = SortedSampler.objects.create(
            sorting_key="text",
            is_ascending=True,
            project=self.project,
        )
        self.documents = Document.objects.filter(pk__in=(6, 7, 8))


    def test_sample(self):
        self.assertEqual(
            self.sorted_sampler.sample(documents=self.documents, target_num_documents=3).values_list('id', flat=True),
            [7, 6, 8]
        )

        self.sorted_sampler.is_ascending = False
        self.sorted_sampler.save()

        self.assertEqual(
            self.sorted_sampler.sample(documents=self.documents, target_num_documents=3).values_list('id', flat=True),
            [8, 6, 7]
        )

