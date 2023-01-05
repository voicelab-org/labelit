from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from labelit.storages import image_storage
import os
from django.http import JsonResponse, HttpResponse


class ImageUpload(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        file_obj = request.FILES.get("image", "")
        # TODO: validate file

        file_directory_within_bucket = ""

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket, file_obj.name
        )

        image_storage.save(file_path_within_bucket, file_obj)
        file_url = "/download_image/" + file_obj.name

        # HACK
        # file_url = "http://0.0.0.0:8000" + file_url

        return JsonResponse(
            {
                "message": "OK",
                "url": file_url,
            }
        )

        """
        if not image_storage.exists(file_path_within_bucket):  # avoid overwriting existing file
            image_storage.save(file_path_within_bucket, file_obj)
            file_url = "/api/download_image/"+file_obj.name

            # HACK
            file_url = "http://0.0.0.0:8000" + file_url

            return JsonResponse({
                'message': 'OK',
                'url': file_url,
            })
        else:
            return JsonResponse({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=image_storage.bucket_name
                ),
            }, status=400)
        """


class ImageDownload(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, filename):

        if image_storage.exists(filename):
            file = image_storage.open(filename, "rb")
            response = HttpResponse(
                file.read(), content_type="image/" + filename.split(".")[1]
            )
            response["Content-Disposition"] = "inline; filename=" + filename
            return response
