from labelit.storages import audio_storage
import json
import os
from django.db import transaction
from labelit.utils.audio_utils import get_audio_duration_in_seconds
from labelit.models import Document, Dataset

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatasetImporter:
    def __init__(
        self, path_to_uploaded_directory: str, allow_not_present_files: bool = True
    ):
        self.dir_path = path_to_uploaded_directory
        self.allow_not_present_files = allow_not_present_files

    def _validate(self):
        # TODO: implement
        pass

    @transaction.atomic
    def _import(self):
        metadata = json.load(open(os.path.join(self.dir_path, "meta.json")))
        assert "name" in metadata.keys()
        dataset = Dataset.objects.create(
            name=metadata.get("name"),
            metadata=metadata,
        )

        def _import_documents():
            documents_dir_path = os.path.join(self.dir_path, "documents")

            filenames = list(os.listdir(documents_dir_path))
            document_names = list(
                set(
                    map(
                        lambda x: ".".join(x.replace(".meta", "").split(".")[:-1]),
                        filenames,
                    )
                )
            )
            for idx, doc_name in enumerate(document_names):
                logger.info(f"Document import: {idx}/{len(document_names)}")
                doc_dict = dict(
                    dataset=dataset,
                )
                audio_name = f"{doc_name}.wav"
                metadata_name = f"{doc_name}.meta.json"
                text_name = f"{doc_name}.txt"

                with open(os.path.join(documents_dir_path, metadata_name), "r") as f:
                    metadata = json.load(f)

                if audio_name in filenames or self.allow_not_present_files:
                    doc_dict["audio_filename"] = audio_name
                    source_audio_path = os.path.join(documents_dir_path, audio_name)
                    if metadata.get("audio_duration", None):
                        doc_dict["audio_duration"] = metadata["audio_duration"]
                    else:
                        doc_dict[
                            "audio_duration"
                        ] = 1000 * get_audio_duration_in_seconds(source_audio_path)

                if text_name in filenames:
                    with open(os.path.join(documents_dir_path, text_name)) as f:
                        doc_dict["text"] = f.read()

                Document.objects.create(**doc_dict)

        logger.info("Importing documents...")
        _import_documents()

        dataset_docs = Document.objects.filter(dataset=dataset)

        def _upload_audio_to_storage():
            audio_doc_names = list(
                dataset_docs.values_list("audio_filename", flat=True)
            )

            for idx, audio_name in enumerate(audio_doc_names):
                logger.info(f"Audio import: {idx}/{len(audio_doc_names)}")
                audio_path = os.path.join(self.dir_path, "documents", audio_name)

                if os.path.exists(audio_path):
                    with open(audio_path, "rb") as file_reader:
                        writer = audio_storage.open(audio_name, "w")
                        writer.write(file_reader.read())
                        writer.close()

        logger.info("Uploading audios...")
        _upload_audio_to_storage()

    def import_dataset(self):
        self._validate()
        self._import()
