from labelit.storages import audio_storage as storage
import os
from botocore.exceptions import ClientError

import logging
logger = logging.getLogger(__name__)


def check_file_exists(key, current_storage=storage):
    try:
        current_storage.connection.meta.client.head_object(
            Bucket=current_storage.bucket_name, Key=key
        )
    except ClientError as err:
        if err.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            return False
        else:
            raise

    return True


def upload_folder_to_s3_bucket_folder(source_path, dest_prefix, current_storage=storage):
    for root, dirs, files in os.walk(source_path):
        for file in files:
            relative_path = ""
            if root != source_path:
                relative_path = os.path.relpath(root, source_path)
            key = os.path.join(dest_prefix, relative_path, file)

            try:
                current_storage.bucket.upload_file(os.path.join(root, file), key)
            except ClientError as e:
                logger.error(e)
                return False

    return True
