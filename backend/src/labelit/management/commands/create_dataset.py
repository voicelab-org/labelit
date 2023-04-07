import os
import shlex
from tqdm import tqdm
from itertools import chain
from distutils.util import strtobool
from subprocess import check_call, check_output

from django.core.management.base import BaseCommand

from labelit.management.scripts.cutfile import treat_onefile
from labelit.models import Document, DocumentSequence, Dataset
from labelit.storages import audio_storage, SourceAudioStorage


import tempfile

MAX_FILES = int(os.getenv("MAX_DOWNLOADED_FILES_PER_RUN", 20))


def ffmpeg(target_filename, input_filename, **kwargs):
    """Convert audio files using ffmpeg.

    Args:
        target_filename (str):  A file name to be created as the result of the conversion.
        input_filename (str):  A file name to use as input
        **kwargs:  Arbitrary keyword arguments to be passed to ffmpeg.

    Returns:
        None

    Raises:
        FileNotFoundError:  If ffmpeg binary is not found in the PATH.
        subprocess.CalledProcessError:  If ffmpeg returns with a non-0 exit code.
    """
    named_args = list(
        chain(*(("-%s" % key, str(value)) for key, value in kwargs.items()))
    )
    cmd = (
        shlex.split("ffmpeg -y -loglevel error -i")
        + [input_filename]
        + named_args
        + [target_filename]
    )
    check_call(cmd)  # raises a CalledProcessError exception if ffmpeg returns non 0


def sox_normalize(input_filename, target_filename):
    cmd = [
        "sox",
        input_filename,
        target_filename,
        "compand",
        "0.3,0.8",
        "6:-70,-60,-10",
        "-15",
        "-75",
        "0.2",
        "norm",
        "-0.1",
    ]
    check_call(cmd)


def process_single_new_file(filename, dataset, source_audio_storage):
    """Process a call recording file from the source AWS S3 bucket by file name.

    A call recording file will be downloaded, registered as a `DocumentSequence` record in the
    database, and then split into several segments (WAV files).

    For each segment, it will be converted into MP3 file, uploaded into a target
    AWS S3 bucket, and a `Document` record will be created in the database.

    //The source file will be deleted from AWS S3 bucket after if has been processed.

    Args:
        filename (str):  An AWS S3 bucket's Key (file name) of a file to be processed.
        dataset (object) : Dataset object to which documents will be included
        source_audio_storage: AWS S3 bucket source storage
    Returns:
        None
    """
    # Auto-delete local files when done
    with tempfile.TemporaryDirectory() as tmp_dirname:
        mp3_files = []
        local_filename = os.path.join(tmp_dirname, filename)
        source_audio_storage.open(filename, "rb").obj.download_file(local_filename)

        # Detect stereo files
        num_channels = 1
        infos_file = (
            check_output(
                ["ffprobe", "-i", local_filename, "-show_streams", "-loglevel", "quiet"]
            )
            .decode()
            .split("\n")
        )
        for one_info in infos_file:
            if one_info.startswith("channels="):
                num_channels = int(one_info.strip().split("=")[1])
                break

        # Convert to normalized WAV format
        if num_channels == 1:
            wav_filename = local_filename + "_conv.wav"
            ffmpeg(wav_filename, local_filename, codec="pcm_s16le")

            # VAD analysis + generate separated audio segments
            list_segs = list(treat_onefile(wav_filename))

            # Create a new DocumentSequence object
            new_document_sequence, _ = DocumentSequence.objects.get_or_create(
                name=filename, dataset=dataset, num_documents=len(list_segs)
            )

            for seq_no, seq_start, seq_end, seq_filename in list_segs:
                # Convert to MP3
                mp3_filename = "%s.mp3" % (os.path.splitext(seq_filename)[0],)
                ffmpeg(
                    mp3_filename, seq_filename, codec="libmp3lame", **{"qscale:a": 0}
                )
                remote_filename = os.path.basename(mp3_filename)

                # Create an Audio record in the database
                # TODO: add audio duration
                Document.objects.create(
                    dataset=dataset,
                    document_sequence=new_document_sequence,
                    audio_filename=remote_filename,
                    sequence_index=seq_no,
                )

                # Upload into the target AWS S3 bucket
                audio_storage.open(remote_filename, "wb").obj.upload_file(mp3_filename)
                mp3_files.append(mp3_filename)

                # try:
                #     if os.environ['SCRIBER_PERFORM_COMPRESSION']:
                #         # Compute & store a compressed version
                #         compressed_wav_filename = '%s_COMPRESSED.wav' % (os.path.splitext(seq_filename)[0],)
                #         compressed_mp3_filename = '%s_COMPRESSED.mp3' % (os.path.splitext(seq_filename)[0],)

                #         # Normalize & convert to MP3
                #         sox_normalize(seq_filename, compressed_wav_filename)
                #         ffmpeg(compressed_mp3_filename, compressed_wav_filename, codec='libmp3lame', **{'qscale:a': 0})

                #         # Auto-delete files when done
                #         stack.callback(os.remove, compressed_mp3_filename)
                #         stack.callback(os.remove, compressed_wav_filename)

                #         # Upload into the target AWS S3 bucket
                #         remote_filename = os.path.basename(compressed_mp3_filename)
                #         audio_storage.open(remote_filename, 'wb').obj.upload_file(compressed_mp3_filename)
                # except KeyError:
                #     pass

        else:
            for chan_index in range(num_channels):
                wav_filename = (
                    local_filename + "_conv_channel_" + str(chan_index) + ".wav"
                )
                ffmpeg(
                    wav_filename,
                    local_filename,
                    af=("pan=mono|c0=c" + str(chan_index)),
                    codec="pcm_s16le",
                )

                # VAD analysis + generate separated audio segments
                list_segs = list(treat_onefile(wav_filename))

                # Create a new DocumentSequence object
                new_document_sequence, _ = DocumentSequence.objects.get_or_create(
                    name=filename, dataset=dataset, num_documents=len(list_segs)
                )

                for seq_no, seq_start, seq_end, seq_filename in list_segs:
                    # Convert to MP3
                    mp3_filename = "%s.mp3" % (os.path.splitext(seq_filename)[0],)
                    ffmpeg(
                        mp3_filename,
                        seq_filename,
                        codec="libmp3lame",
                        **{"qscale:a": 0}
                    )
                    remote_filename = os.path.basename(mp3_filename)

                    # Create a Document record in the database
                    Document.objects.create(
                        dataset=dataset,
                        document_sequence=new_document_sequence,
                        audio_filename=remote_filename,
                        sequence_index=seq_no,
                    )

                    # Upload into the target AWS S3 bucket
                    audio_storage.open(remote_filename, "wb").obj.upload_file(
                        mp3_filename
                    )
                    mp3_files.append(mp3_filename)

                    # try:
                    #     if os.environ['SCRIBER_PERFORM_COMPRESSION']:
                    #         # Compute & store a compressed version
                    #         compressed_wav_filename = '%s_COMPRESSED.wav' % (os.path.splitext(seq_filename)[0],)
                    #         compressed_mp3_filename = '%s_COMPRESSED.mp3' % (os.path.splitext(seq_filename)[0],)

                    #         # Normalize & convert to MP3
                    #         sox_normalize(seq_filename, compressed_wav_filename)
                    #         ffmpeg(compressed_mp3_filename, compressed_wav_filename, codec='libmp3lame', **{'qscale:a': 0})

                    #         # Auto-delete files when done
                    #         stack.callback(os.remove, compressed_mp3_filename)
                    #         stack.callback(os.remove, compressed_wav_filename)

                    #         # Upload into the target AWS S3 bucket
                    #         remote_filename = os.path.basename(compressed_mp3_filename)
                    #         audio_storage.open(remote_filename, 'wb').obj.upload_file(compressed_mp3_filename)
                    # except KeyError:
                    #     pass

        dataset.save()


class Command(BaseCommand):
    help = """Load data from AWS S3 bucket into the database.
    
    Usage example:
           
    `python manage.py create_dataset \
        --dataset-name new_dataset_$(date +%s) \
        --source-bucket-name source-bucket \
        --aws-key-id ${AWS_ACCESS_KEY_ID} \
        --aws-key-content ${AWS_SECRET_ACCESS_KEY} \
        --is-streamed true`
"""

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--max-files",
            type=int,
            default=MAX_FILES,
            dest="max_files",
            help="Download and process up to MAX_FILES files (Default: %(default)s)",
        )

        parser.add_argument(
            "--dataset-name",
            type=str,
            required=True,
            dest="dataset_name",
            help="Name of the dataset to be created",
        )

        parser.add_argument(
            "--source-bucket-name",
            type=str,
            required=True,
            dest="source_bucket_name",
            help="Name of the source S3 bucket",
        )

        parser.add_argument(
            "--aws-key-id",
            type=str,
            required=True,
            dest="aws_key_id",
            help="AWS key ID",
        )

        parser.add_argument(
            "--aws-key-content",
            type=str,
            required=True,
            dest="aws_key_content",
            help="AWS key content",
        )

    def handle(self, *args, **options):
        source_audio_storage = SourceAudioStorage(
            source_audio_storage_bucket_name=options["source_bucket_name"],
            aws_key_id=options["aws_key_id"],
            aws_key_content=options["aws_key_content"],
        )

        dataset = Dataset.objects.create(name=options["dataset_name"])
        _directories, files = source_audio_storage.listdir(".")
        for filename in tqdm(files[: options["max_files"]]):
            if DocumentSequence.objects.filter(name=filename).exists():
                continue
            process_single_new_file(filename, dataset, source_audio_storage)
