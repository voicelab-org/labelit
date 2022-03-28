from django.test import TestCase
from labelit.models import Dataset
from labelit.serializers import DatasetSerializer


class DatasetSerializerTests(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="IMDB reviews",
        )
        self.serializer1 = DatasetSerializer(
            instance=self.dataset
        )

    def test_contains_expected_fields_and_specific_fields_and_resourcetype(self):
        self.assertEqual(
            set(self.serializer1.data.keys()),
            set([
                'id',
                'name',
            ])
        )
