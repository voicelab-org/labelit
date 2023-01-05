from labelit.storages import audio_storage
import json
import os
from django.db import transaction
from labelit.utils.audio_utils import get_audio_duration_in_seconds
from labelit.models import Document, Dataset


class DatasetImporter:
    def __init__(
        self,
        path_to_uploaded_directory: str,
    ):
        self.dir_path = path_to_uploaded_directory

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
            document_names = list(set(map(lambda x: x.split(".")[0], filenames)))
            for doc_name in document_names:
                doc_dict = dict(
                    dataset=dataset,
                )
                audio_name = f"{doc_name}.wav"
                text_name = f"{doc_name}.txt"
                if audio_name in filenames:
                    doc_dict["audio_filename"] = audio_name
                    source_audio_path = os.path.join(documents_dir_path, audio_name)
                    doc_dict["audio_duration"] = 1000 * get_audio_duration_in_seconds(
                        source_audio_path
                    )

                if text_name in filenames:
                    with open(os.path.join(documents_dir_path, text_name)) as f:
                        doc_dict["text"] = f.read()
                Document.objects.create(**doc_dict)

        _import_documents()

        dataset_docs = Document.objects.filter(dataset=dataset)

        def _upload_audio_to_storage():
            audio_doc_names = list(
                dataset_docs.values_list("audio_filename", flat=True)
            )
            for audio_name in audio_doc_names:
                audio_path = os.path.join(self.dir_path, "documents", audio_name)
                # logger.debug(f"&type of audio_storage.open(audio_path, 'wb').obj: {type(audio_storage.open(audio_path, 'wb').obj)}")
                # audio_storage.open(audio_path, "rb").obj.upload_file(f"{audio_name}/")
                with open(audio_path, "rb") as file_reader:

                    writer = audio_storage.open(audio_name, "w")
                    writer.write(file_reader.read())
                    writer.close()

        _upload_audio_to_storage()

    def import_dataset(self):
        self._validate()
        self._import()
