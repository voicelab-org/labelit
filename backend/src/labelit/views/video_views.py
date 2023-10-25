import os
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from botocore.exceptions import ClientError
from rest_framework import viewsets
from rest_framework.decorators import action

from labelit.models import Document
from labelit.storages import video_storage as storage


from django.conf import settings
from django.http import JsonResponse

import logging

logger = logging.getLogger(__name__)


class VideoViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Document.objects

    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    def _check_file_is_reachable(self, video_filename):
        head = None
        try:
            head = storage.connection.meta.client.head_object(
                Bucket=storage.bucket_name, Key=video_filename
            )
        except ClientError as err:
            if err.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                # respond with HTTP 404 if the requested file does not exist
                raise Http404
            elif err.response["ResponseMetadata"]["HTTPStatusCode"] == 403:
                # respond with HTTP 403 if access is Forbidden (CORS?)
                logger.error(
                    f"Access forbidden to {video_filename}. Is CORS properly configured?"
                )
            else:
                raise  # Let it bubble up if it was some other error

        return head

    @action(methods=["GET"], detail=True)
    def serve_url(self, request, pk, format=None):
        video_document = self.get_object(pk)
        head_obj = self._check_file_is_reachable(video_document.video_filename)

        video_filename = video_document.video_filename
        print("&video_filename", video_filename)
        url = storage.connection.meta.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": storage.bucket_name, "Key": video_filename},
            ExpiresIn=settings.SEGMENT_EXPIRATION_TIME_IN_SECONDS,
        )

        data = {}

        if os.environ.get("AWS_S3_OPTIONS", "") == "local":
            url = url.replace("minio", "localhost")

        data["url"] = url
        data["size"] = head_obj["ContentLength"]
        response = JsonResponse(data)
        # One week cache
        response[
            "Cache-Control"
        ] = f"private, max-age={settings.SEGMENT_EXPIRATION_TIME_IN_SECONDS}, immutable"

        return response
