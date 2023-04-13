import os
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject, cached_property

storage_class = get_storage_class(os.environ.get("AUDIO_FILE_STORAGE"))


class ImageStorage(LazyObject):
    @cached_property
    def storage_class(self):
        return get_storage_class(os.environ.get("IMAGE_FILE_STORAGE"))

    def _setup(self):
        self._wrapped = self.storage_class(
            bucket_name=os.environ.get("AWS_IMAGE_STORAGE_BUCKET_NAME")
        )


class AudioStorage(LazyObject):
    @cached_property
    def storage_class(self):
        return get_storage_class(os.environ.get("AUDIO_FILE_STORAGE"))

    def _setup(self):
        self._wrapped = self.storage_class(
            bucket_name=os.environ.get("AWS_AUDIO_STORAGE_BUCKET_NAME")
        )


class VideoStorage(LazyObject):
    @cached_property
    def storage_class(self):
        return get_storage_class(os.environ.get("VIDEO_FILE_STORAGE"))

    def _setup(self):
        self._wrapped = self.storage_class(
            bucket_name=os.environ.get("AWS_VIDEO_STORAGE_BUCKET_NAME")
        )


class SourceAudioStorage(storage_class):
    def __init__(self, source_audio_storage_bucket_name, aws_key_id, aws_key_content):
        self.bucket_name = source_audio_storage_bucket_name
        self.access_key = aws_key_id
        self.secret_key = aws_key_content
        super().__init__()


# create lazy objects which would be initialized on a call (we need this for settings availability)
audio_storage = AudioStorage()
image_storage = ImageStorage()
