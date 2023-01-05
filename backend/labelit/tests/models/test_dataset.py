from django.test import TestCase
from labelit.models import (
    Project,
    CategoricalTask,
    OrdinalTask,
    OrdinalLabel,
    Dataset,
    Batch,
    Document,
    Annotation,
)

import os
from labelit.storages import audio_storage
from labelit.utils.s3_utils import check_file_exists

from django.core.files.storage import FileSystemStorage

from unittest.mock import patch
import tempfile

fs_storage = None
with tempfile.TemporaryDirectory() as tmp_dirname:
    FileSystemStorage(location=tmp_dirname)


@patch("labelit.storages.audio_storage", fs_storage)
class DatasetModelTests(TestCase):
    def setUp(self):
        self.dataset = Dataset.objects.create(name="IMDB")

        audio_storage.bucket.upload_file(
            os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.mp3"),
            "sample_data.mp3",
        )

        self.document = Document.objects.create(
            text="lovediit", audio_filename="sample_data.mp3", dataset=self.dataset
        )

    def test_hls_signal(self):
        self.dataset.is_streamed = True
        self.dataset.save()

        self.assertTrue(check_file_exists(self.document.hls_audio_file_key))
