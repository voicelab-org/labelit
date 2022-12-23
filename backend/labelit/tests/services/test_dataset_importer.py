from django.test import TestCase
from django.contrib.auth import get_user_model

from labelit.utils.agreement_metrics.ordinal_alpha import OrdinalAlphaMetric
from labelit.models import Dataset, Document
from users.models import User


from labelit.storages import audio_storage
from labelit.services.dataset_importer import DatasetImporter


class DatasetImporterTests(TestCase):
    fixtures = []  #'test_data'

    def setUp(self):
        # self.u1 = User.objects.all().first()
        # self.u2 = User.objects.all()[1]
        self.source_dir_path = 'labelit/tests/data/example_dataset'

    def test_dataset_is_correctly_imported(self):
        dataset_importer = DatasetImporter(self.source_dir_path)
        dataset_importer.import_dataset()

        # dataset object exists
        try:
            ds = Dataset.objects.get(name="My dummy dataset")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        # dataset has all the metadata
        expected_metadata = json.load(open(os.path.join(self.source_dir_path, 'meta.json')))
        self.assertEqual(
            ds.meta,
            expected_metadata,
        )

        # document objects exist
        docs = Document.objects.filter(dataset=ds)
        self.assertEqual(
            docs.counts(),
            2,
        )

        # audios are stored in the storage backend
        self.assertEqual(
            set(list(docs.values_list('audio_filename'))),
            set(['file1.wav', 'file2.wav'])
        )
        for doc in docs:
            self.assertTrue(
                audio_storage.exists(doc.audio_filename)
            )




