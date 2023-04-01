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


def generate_dynamic_waveform_from_audio(input_file, output_file, create_folder=False):
    """Given an audio file, it generates its waveform and stores it into a .json file"""

    if create_folder:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    output_waveform = os.path.splitext(input_file)[0] + "_waveform.json"
    subprocess.call(
        [
            "audiowaveform",
            "-i",
            input_file,
            "-o",
            output_waveform,
            "--pixels-per-second",
            "100",
            "-b",
            "8",
            "-q",
        ]
    )

    with open(output_waveform) as json_file:
        json_waveform = json.load(json_file)

    a = np.array(json_waveform["data"])
    # datascale = np.array(json_waveform['data'])/126

    datascale = np.where(a > 0, a / (max(a) + 1), a / (abs(min(a)) + 1))
    json_waveform["waveform"] = datascale.tolist()
    del json_waveform["data"]

    with open(output_waveform, "w") as outfile:
        json.dump(json_waveform, outfile)


def generate_waveform_for_dataset(dataset_name):
    """generate waveform json for all the files in the dataset"""
    from labelit.models import Document

    audio_files_queryset = Document.objects.filter(dataset__name=dataset_name)
    audio_files = {
        file for file in audio_files_queryset.values_list("audio_filename", flat=True)
    }

    progress_bar = tqdm(audio_files)
    for audio_file_name in progress_bar:
        progress_bar.set_description(f"Generating Wave Peaks for {audio_file_name}...")
        waveform_audio_file_name = (
            os.path.splitext(audio_file_name)[0] + "_waveform.json"
        )

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
                    create_folder=False,
                )

                storage.bucket.upload_file(
                    waveform_audio_file_name, waveform_audio_file_name
                )
                try:
                    os.remove(audio_file_name)
                    os.remove(waveform_audio_file_name)
                except:
                    pass
