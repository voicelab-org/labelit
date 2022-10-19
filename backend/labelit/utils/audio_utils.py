from tqdm import tqdm
import tempfile
import os
import subprocess
import shutil
import math
import librosa
import numpy as np
import json
import m3u8
import audiofile

from django.conf import settings
from labelit.storages import audio_storage as storage
from labelit.utils.s3_utils import upload_folder_to_s3_bucket_folder, check_file_exists


import logging
logger = logging.getLogger(__name__)


def get_ffmpeg_command():
    """Gets the ffmpeg binary in the host machine."""

    ffmpeg_path = shutil.which('ffmpeg')
    return ffmpeg_path if ((ffmpeg_path is not None) and len(ffmpeg_path)) else shutil.which('avconv')


def get_ffprobe_command():
    """Gets the ffprobe binary in the host machine."""

    ffprobe_path = shutil.which('ffprobe')
    return ffprobe_path if ((ffprobe_path is not None) and len(ffprobe_path)) else shutil.which('avprobe')


def get_audio_duration_in_seconds(file_name):
    """ Retrieves the duration of a file """

    return float(subprocess.check_output(
        [get_ffprobe_command(),
         '-v', 'error',
         '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1',
         file_name
         ]).decode())


def generate_waveform_from_audio(input_file, output_file, create_folder=False):
    """ Given an audio file, it generates its waveform and stores it into a .json file """

    if create_folder:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    signal, sr = audiofile.read(input_file)
    signal =  np.average(signal, axis=0)
    duration = len(signal)/sr
    num_chunks = int(math.ceil(duration/120.))
    chunk_size = duration/num_chunks
    points_per_chunk = round(float(settings.NUM_ELEMENTS_IN_WAVEFORM)/num_chunks)
    waveform_intermediate = []
    for idx_chunk in range(num_chunks):
        signal_chunk = signal[int(idx_chunk*chunk_size)*sr:int((idx_chunk*chunk_size)+chunk_size)*sr]
        waveform_intermediate += [resampled_val for resampled_val in signal_chunk[[round(index) for index in np.linspace(0, len(signal_chunk)-1, points_per_chunk)]]]
    
    np_waveform_intermediate = np.array(waveform_intermediate)
    waveform = [float(resampled_val) for resampled_val in np_waveform_intermediate[[round(index) for index in np.linspace(0, len(np_waveform_intermediate)-1, int(settings.NUM_ELEMENTS_IN_WAVEFORM))]]]

    waveform_info = {
        "duration": duration,
        "waveform": waveform
    }

    with open(output_file, "w") as f:
        json.dump(waveform_info, f)



def generate_hls_from_audio(input_file, output_file, create_folder=False, generate_waveform=True):
    """ Given an audio file, it generates and HLS playlist """

    segments_folder = os.path.join(os.path.dirname(output_file), "segments")

    if create_folder:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        os.makedirs(segments_folder, exist_ok=True)

    cmd = [
        get_ffmpeg_command(),
        '-y',
        '-i', input_file,
        '-copyts',
        '-acodec', 'libmp3lame',
        '-ar', '8000',
        '-q:a', '9',
        '-f', 'hls',
        '-hls_playlist_type', 'vod',
        '-hls_time', "6", # Size of segments
        '-hls_allow_cache', '1',
        '-hls_flags',
        'second_level_segment_index+second_level_segment_size+second_level_segment_duration+round_durations',
        '-strftime', '1',
        '-strftime_mkdir', '1',
        '-hls_segment_filename', 'segments/segment_%Y%m%d%H%M%S_%%04d_%%08s_%%013t.mp3',
        '-threads', str(max(1, os.cpu_count() - 1)),
        '-loglevel', 'quiet',
        output_file
    ]

    subprocess.call(cmd, cwd=os.path.dirname(output_file))

    if generate_waveform:
        generate_waveform_from_audio(input_file=input_file,
                                     output_file=os.path.join(os.path.dirname(output_file), "waveform.json"),
                                     create_folder=False)


def convert_and_upload_single_file(audio_file_name, hls_file_name, hls_file_key,
                                   audio_file_key=None, generate_waveform=True):
    """ Converts a single file to HLS and uploads it to the bucket."""

    if not check_file_exists(hls_file_key):
        if audio_file_key:
            storage.bucket.download_file(audio_file_key, audio_file_name)

        generate_hls_from_audio(audio_file_name, hls_file_name, create_folder=True, generate_waveform=generate_waveform)

        upload_folder_to_s3_bucket_folder(source_path=os.path.dirname(hls_file_name),
                                          dest_prefix=os.path.dirname(hls_file_key))
    else:
        logger.warning(f"File {hls_file_key} already in bucket. Skipping...")

def generate_waveform_for_dataset(dataset_name):
    """ Converts all the files in the dataset to HLS (ignores them if they have been already converted in the past)"""
    from labelit.models import Document
    audio_files_queryset = Document.objects.filter(dataset__name=dataset_name)
    audio_files = {file for file in audio_files_queryset.values_list("audio_filename", flat=True)}

    progress_bar = tqdm(audio_files)
    for audio_file_name in progress_bar:
        progress_bar.set_description(f"Uploading {audio_file_name}...")
        waveform_audio_file_name = os.path.splitext(audio_file_name)[0]+'_waveform.json'
        if not check_file_exists(waveform_audio_file_name): # checkwaveform 
            storage.bucket.download_file(audio_file_name, audio_file_name)
            generate_waveform_from_audio(input_file=audio_file_name,
                                        output_file=waveform_audio_file_name,
                                        create_folder=False)
            
            storage.bucket.upload_file(waveform_audio_file_name,waveform_audio_file_name)



def file_key_to_hls_file_key(file_key):
    """ Given a key, obtains the expected playlist."""
    return os.path.join("hls", file_key, "playlist.m3u")


def convert_raw_to_hls(audio_file_key):
    """Converts a raw file into HLS"""

    logger.debug(f"Converting file {audio_file_key}...")
    with tempfile.TemporaryDirectory() as tmp_dirname:
        audio_file_name = os.path.join(tmp_dirname, audio_file_key)
        file_key = os.path.splitext(audio_file_key)[0]
        hls_file_key = file_key_to_hls_file_key(file_key)
        hls_file_name = os.path.join(tmp_dirname, hls_file_key)

        convert_and_upload_single_file(audio_file_name=audio_file_name,
                                       hls_file_name=hls_file_name,
                                       hls_file_key=hls_file_key,
                                       audio_file_key=audio_file_key,
                                       generate_waveform=True)

        return hls_file_key


def check_hls_is_correct(playlist_key):
    """Checks that a file currently in the bucket is fully playable."""

    playlist_uri = file_key_to_hls_file_key(playlist_key)
    if not check_file_exists(playlist_uri):
        return False
    if not check_file_exists(os.path.join(os.path.dirname(playlist_uri), "waveform.json")):
        return False

    with tempfile.TemporaryDirectory() as tmp_dirname:
        local_playlist_file = os.path.join(tmp_dirname, "playlist.m3u")
        storage.bucket.download_file(playlist_uri, local_playlist_file)

        playlist = m3u8.load(local_playlist_file)
        for segment in playlist.segments:
            if not check_file_exists(os.path.join(os.path.dirname(playlist_uri), segment.uri)):
                return False

    return True


def gather_valid_hls(hls_files):
    """
    Checks all the HLS playlist have the expected files in it, to avoid the case in which the conversion was stopped for
    some reason.
    """

    valid_hls_files = set()
    for playlist_key in hls_files:
        if check_hls_is_correct(playlist_key):
            valid_hls_files.add(playlist_key)

    return valid_hls_files


def convert_files_in_dataset_to_hls(dataset_name):
    """ Converts all the files in the dataset to HLS (ignores them if they have been already converted in the past)"""
    from labelit.models import Document
    audio_files_queryset = Document.objects.filter(dataset__name=dataset_name)

    audio_files = {os.path.splitext(file)[0]: file
                   for file in audio_files_queryset.values_list("audio_filename", flat=True)}

    hls_files = gather_valid_hls(storage.listdir("/hls")[0])

    pending_files = set(audio_files.keys()) - hls_files

    progress_bar = tqdm(pending_files)
    for file_key in progress_bar:
        progress_bar.set_description(f"Uploading {file_key}...")
        convert_raw_to_hls(audio_files[file_key])

    logger.info(f"Nothing left to update. Total files updated: {len(pending_files)}.")

