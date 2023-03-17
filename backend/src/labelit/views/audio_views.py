import os
import json
from django.http import Http404, HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated
from botocore.exceptions import ClientError
from rest_framework import viewsets
from rest_framework.decorators import action

from labelit.models import Document
from labelit.storages import audio_storage as storage
from labelit.utils.audio_utils import check_hls_is_correct, check_file_exists


from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.middleware.gzip import GZipMiddleware

import logging

logger = logging.getLogger(__name__)


class AudioViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Document.objects

    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    def _use_hls(self, audio_document):
        """Are we using HLS? Depends on the configuration and/or the availability of the file."""
        if not audio_document.dataset.is_streamed:
            return False

        if not check_file_exists(audio_document.hls_audio_file_key):
            return False

        if not check_hls_is_correct(audio_document.hls_audio_file_key.split("/")[1]):
            return False

        return True

    def _check_file_is_reachable(self, audio_filename):
        head = None
        try:
            head = storage.connection.meta.client.head_object(
                Bucket=storage.bucket_name, Key=audio_filename
            )
        except ClientError as err:
            if err.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                # respond with HTTP 404 if the requested file does not exist
                raise Http404
            elif err.response["ResponseMetadata"]["HTTPStatusCode"] == 403:
                # respond with HTTP 403 if access is Forbidden (CORS?)
                logger.error(
                    f"Access forbidden to {audio_filename}. Is CORS properly configured?"
                )
            else:
                raise  # Let it bubble up if it was some other error

        return head

    def _serve_file(self, segment_key):
        """Directly serve a file. Used for serving segments or single files"""
        # Not using presigned urls, serving it directly from Minio or a public bucket
        if settings.S3_DIRECT_SERVE:
            # A pre-signed URL is generated, so the client is redirected. This url is cached to avoid continuous requests
            # from the user side.
            url = storage.connection.meta.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": storage.bucket_name, "Key": segment_key},
                ExpiresIn=settings.SEGMENT_EXPIRATION_TIME_IN_SECONDS,
            )
            if os.environ.get("AWS_S3_OPTIONS", "") == "local":
                url = url.replace("minio", "localhost")
            response = HttpResponseRedirect(url)
            # Added so avoid unnecessary requests to the django server if the user reloads or it has been there in the
            # past 0.75 * SEGMENT_EXPIRATION_TIME_IN_SECONDS
            response["Cache-Control"] = "max-age=%d" % int(
                0.75 * settings.SEGMENT_EXPIRATION_TIME_IN_SECONDS
            )

            return response
        # Using presigned urls --> A redirection with a temporary link is sent to the browser
        else:
            segment = storage.connection.meta.client.get_object(
                Bucket=storage.bucket_name, Key=segment_key
            )
            segment_data = segment["Body"].read()

            response = HttpResponse(content=segment_data)
            response["Content-Type"] = "binary/octet-stream"
            response["Cache-Control"] = "max-age=%d" % int(
                0.75 * settings.SEGMENT_EXPIRATION_TIME_IN_SECONDS
            )

            return response

    def retrieve(self, request, pk, format=None):
        """Gets the playlist of the file, depending on the case"""
        audio_document = self.get_object(pk)

        # Checking which audio format we will be using
        use_hls = self._use_hls(audio_document)
        if use_hls:
            audio_filename = audio_document.hls_audio_file_key
        else:
            audio_filename = audio_document.audio_filename

        head = self._check_file_is_reachable(audio_filename)
        if not head:
            return HttpResponseForbidden(f"Access forbidden to {audio_filename}.")

        # Serve HLS
        if use_hls:


            def get_response(request):
                playlist = storage.connection.meta.client.get_object(
                    Bucket=storage.bucket_name, Key=audio_filename
                )
                data = playlist["Body"].read()
                response = HttpResponse(content=data)
                response["Content-Type"] = "audio/mpegurl"
                response["Content-Disposition"] = f'''attachment; filename="playlist.m3u"'''
                response["Cache-Control"] = "no-cache"
                return response

            response = get_response(request)

            gzip_middleware = GZipMiddleware(get_response)

            return gzip_middleware.process_response(request, response)

        # Serve single file
        else:
            return self._serve_file(audio_filename)

    @action(methods=["GET"], detail=True)
    def is_using_hls(self, request, pk):
        """Indicates if we are going to use HLS for this file."""
        audio_document = self.get_object(pk)

        return JsonResponse({"use_hls": self._use_hls(audio_document)})

    @action(methods=["GET"], detail=True)
    def audio_info(self, request, pk, format=None):
        """Obtains the waveform for the audio, used for visualization."""


        def get_response(request):
            audio_document = self.get_object(pk)

            if not audio_document.dataset.is_streamed:
                raise Http404

            waveform_key = os.path.join(
                os.path.dirname(audio_document.hls_audio_file_key), "waveform.json"
            )

            if not self._check_file_is_reachable(waveform_key):
                return HttpResponseForbidden(f"Access forbidden to {waveform_key}.")

            # The playlist is sent directly to the user (in this case, no redirection is needed)
            waveform = storage.connection.meta.client.get_object(
                Bucket=storage.bucket_name, Key=waveform_key
            )
            data = json.loads(waveform["Body"].read().decode("utf-8"))
            response = JsonResponse(data)
            # One week cache
            response["Cache-Control"] = "private, max-age=604800, immutable"
            return response

        gzip_middleware = GZipMiddleware(get_response)

        response = get_response(request)

        return gzip_middleware.process_response(request, response)

    @action(methods=["GET"], detail=True)
    def serve_url(self, request, pk, format=None):
        """Obtains the waveform for the audio, used for visualization."""
        audio_document = self.get_object(pk)

        # Checking which audio format we will be using
        use_hls = self._use_hls(audio_document)
        audio_filename = audio_document.audio_filename
        url = storage.connection.meta.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": storage.bucket_name, "Key": audio_filename},
            ExpiresIn=settings.SEGMENT_EXPIRATION_TIME_IN_SECONDS,
        )
        try:
            waveform = storage.connection.meta.client.get_object(
                Bucket=storage.bucket_name,
                Key=audio_filename.split(".")[-2] + "_waveform.json",
            )
            data = json.loads(waveform["Body"].read().decode("utf-8"))
        except:
            data = {"duration": 0, "waveform": None}

        if os.environ.get("AWS_S3_OPTIONS", "") == "local":
            url = url.replace("minio", "localhost")

        data["url"] = url
        response = JsonResponse(data)
        # One week cache
        response[
            "Cache-Control"
        ] = f"private, max-age={settings.SEGMENT_EXPIRATION_TIME_IN_SECONDS}, immutable"
        gzip_middleware = GZipMiddleware(request)
        return gzip_middleware.process_response(request, response)

    @action(methods=["GET"], detail=True, url_path=r"segments/(?P<segment_id>.*\..*)")
    def segments(self, request, pk, segment_id):
        """Obtains the segments"""

        audio_document = self.get_object(pk)

        if not audio_document.dataset.is_streamed:
            raise Http404

        segment_key = os.path.join(
            os.path.dirname(audio_document.hls_audio_file_key), "segments", segment_id
        )

        if not self._check_file_is_reachable(segment_key):
            return HttpResponseForbidden(f"Access forbidden to {segment_key}.")

        return self._serve_file(segment_key)
