from tqdm import tqdm
import os
import subprocess
import shutil
import numpy as np
import json
from django.conf import settings
from labelit.storages import audio_storage as storage
from labelit.utils.s3_utils import upload_folder_to_s3_bucket_folder, check_file_exists


import logging

logger = logging.getLogger(__name__)


def get_ffmpeg_command():
    """Gets the ffmpeg binary in the host machine."""

    ffmpeg_path = shutil.which("ffmpeg")
    return (
        ffmpeg_path
        if ((ffmpeg_path is not None) and len(ffmpeg_path))
        else shutil.which("avconv")
    )


def get_ffprobe_command():
    """Gets the ffprobe binary in the host machine."""

    ffprobe_path = shutil.which("ffprobe")
    return (
        ffprobe_path
        if ((ffprobe_path is not None) and len(ffprobe_path))
        else shutil.which("avprobe")
    )


def get_audio_duration_in_seconds(file_name):
    """Retrieves the duration of a file"""

    return float(
        subprocess.check_output(
            [
                get_ffprobe_command(),
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_name,
            ]
        ).decode()
    )


def generate_dynamic_waveform_from_audio(input_file, output_file):
    """Given an audio file, it generates its waveform and stores it into a .json file"""
    subprocess.call(
        [
            "audiowaveform",
            "-i",
            input_file,
            "-o",
            output_file,
            "--pixels-per-second",
            "100",
            "-b",
            "8",
            "-q",
        ]
    )

    with open(output_file) as json_file:
        json_waveform = json.load(json_file)

    a = np.array(json_waveform["data"])
    # datascale = np.array(json_waveform['data'])/126

    datascale = np.where(a > 0, a / (max(a) + 1), a / (abs(min(a)) + 1))
    json_waveform["waveform"] = datascale.tolist()
    del json_waveform["data"]

    with open(output_file, "w") as outfile:
        json.dump(json_waveform, outfile)


def generate_waveform_for_dataset(dataset_name):
    """generate waveform json for all the files in the dataset"""
    from labelit.models import Document

    audio_files_queryset = Document.objects.filter(dataset__name=dataset_name)
    audio_files = {
        file.audio_filename: file.audio_waveform_json for file in audio_files_queryset
    }

    progress_bar = tqdm(audio_files)
    for doc in progress_bar:
        audio_file_name = doc
        waveform_audio_file_name = audio_files[doc]
        progress_bar.set_description(f"Generating Wave Peaks for {audio_file_name}...")

        try:
            head_obj = check_file_exists(audio_file_name)
        except:
            head_obj = None

        MIN_AUDIO_SIZE_TO_GENERATE_PEAKS = int(
            os.getenv("MIN_AUDIO_SIZE_TO_GENERATE_PEAKS", 4)
        )
        if (
            head_obj
            and head_obj["ContentLength"]
            > MIN_AUDIO_SIZE_TO_GENERATE_PEAKS * 1024 * 1024
        ):
            if not check_file_exists(waveform_audio_file_name):  # checkwaveform
                storage.bucket.download_file(audio_file_name, audio_file_name)
                generate_dynamic_waveform_from_audio(
                    input_file=audio_file_name,
                    output_file=waveform_audio_file_name,
                )

                storage.bucket.upload_file(
                    waveform_audio_file_name, waveform_audio_file_name
                )
                try:
                    os.remove(audio_file_name)
                    os.remove(waveform_audio_file_name)
                except:
                    pass
