from django.test import TestCase
from django.contrib.auth import get_user_model
import json
import m3u8

from rest_framework.test import APIRequestFactory, force_authenticate
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
from labelit.views import AudioViewSet
import os
from labelit.storages import audio_storage

from django.core.files.storage import FileSystemStorage

from unittest.mock import patch
import tempfile

fs_storage = None
with tempfile.TemporaryDirectory() as tmp_dirname:
    FileSystemStorage(location=tmp_dirname)


@patch("labelit.storages.audio_storage", fs_storage)
class AudioViewSetTests(TestCase):
    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.annotator1 = get_user_model().objects.create(
            email="tester@labelit",
            password="tester",
        )
        self.project = Project.objects.create(name="Feelin")
        self.task1 = OrdinalTask.objects.create(
            name="Valence scale",
        )
        self.project.tasks.add(self.task1)
        self.label1 = OrdinalLabel.objects.create(index=0, task=self.task1)
        self.label2 = OrdinalLabel.objects.create(index=1, task=self.task1)
        self.task2 = CategoricalTask.objects.create(
            name="Five emotions",
        )
        self.project.tasks.add(self.task2)
        self.dataset = Dataset.objects.create(name="IMDB")
        self.batch = Batch.objects.create(
            name="Batch 1", dataset=self.dataset, project=self.project
        )

        audio_storage.bucket.upload_file(
            os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.mp3"),
            "sample_data.mp3",
        )

        self.document = Document.objects.create(
            text="lovediit", audio_filename="sample_data.mp3", dataset=self.dataset
        )
        self.batch.documents.add(self.document)

    def _authenticate(self, request):
        force_authenticate(request, user=self.annotator1)

    def test_use_hls(self):
        request = self.request_factory.get("")
        self._authenticate(request)

        self.dataset.is_streamed = False
        self.dataset.save()
        response = AudioViewSet.as_view(
            actions={"get": "is_using_hls"},
        )(request, pk=self.document.id)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["use_hls"], False)
        self.assertEqual(response.status_code, 200)

        self.dataset.is_streamed = True
        self.dataset.save()
        response = AudioViewSet.as_view(
            actions={"get": "is_using_hls"},
        )(request, pk=self.document.id)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["use_hls"], True)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        request = self.request_factory.get("")
        self._authenticate(request)

        self.dataset.is_streamed = False
        self.dataset.save()
        response = AudioViewSet.as_view(
            actions={"get": "retrieve"},
        )(request, pk=self.document.id)
        self.assertEqual(response._headers["content-type"][1], "binary/octet-stream")
        self.assertEqual(response.status_code, 200)

        self.dataset.is_streamed = True
        self.dataset.save()
        response = AudioViewSet.as_view(
            actions={"get": "is_using_hls"},
        )(request, pk=self.document.id)
        self.assertEqual(response._headers["content-type"][1], "application/json")
        self.assertEqual(response.status_code, 200)

    def test_audio_info(self):
        request = self.request_factory.get("")
        self._authenticate(request)

        self.dataset.is_streamed = True
        self.dataset.save()
        response = AudioViewSet.as_view(
            actions={"get": "audio_info"},
        )(request, pk=self.document.id)
        self.assertIn("duration", json.loads(response.content.decode("utf-8")).keys())
        self.assertIn("waveform", json.loads(response.content.decode("utf-8")).keys())
        self.assertEqual(response._headers["content-type"][1], "application/json")
        self.assertEqual(response.status_code, 200)

    def test_segments(self):
        request = self.request_factory.get("")
        self._authenticate(request)

        self.dataset.is_streamed = True
        self.dataset.save()
        response = AudioViewSet.as_view(
            actions={"get": "retrieve"},
        )(request, pk=self.document.id)
        playlist_info = response.content.decode("utf-8")

        playlist = m3u8.loads(playlist_info)
        segment_id = playlist.segments[0].uri.split("/")[1]
        response = AudioViewSet.as_view(
            actions={"get": "segments"},
        )(request, pk=self.document.id, segment_id=segment_id)
        self.assertEqual(response._headers["content-type"][1], "binary/octet-stream")
        self.assertEqual(response.status_code, 200)
