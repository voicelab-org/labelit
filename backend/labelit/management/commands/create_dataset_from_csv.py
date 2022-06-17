from django.core.management.base import BaseCommand
from labelit.models import Document, DocumentSequence, Dataset
import pandas as pd
from distutils.util import strtobool


class Command(BaseCommand):
    help = "Creates a dataset from CSV file"

    def add_arguments(self, parser):

        parser.add_argument(
            "--csv-path",
            type=str,
            required=True,
            dest="csv_file",
            help="CSV file contains dataset info",
        )

        parser.add_argument(
            "--dataset-name",
            type=str,
            required=True,
            dest="dataset_name",
            help="Dataset name to be created",
        )

        parser.add_argument(
            "--is-streamed",
            type=str,
            required=False,
            default=False,
            dest="is_streamed",
            help="Will the files be streamed to the users?",
        )

    def handle(self, *args, **options):

        data = pd.read_csv(options["csv_file"])

        dataset, dataset_created = Dataset.objects.get_or_create(
            name=options["dataset_name"]
        )
        known_doc_seq = set()
        docs_seq = {}
        for index, row in data.iterrows():
            filename = row["basename"]
            if filename not in known_doc_seq:
                known_doc_seq.add(filename)
                docs_seq[filename] = []
            docs_seq[filename].append(
                {
                    "document_index": row["seq_index"],
                    "duration": row["duration"],
                    "text": row["text"],
                    "audio_filename": row["audio_filename"],
                }
            )
        for doc_seq_name in docs_seq:
            document_sequence, created = DocumentSequence.objects.get_or_create(
                name=doc_seq_name, dataset=dataset
            )
            docs = sorted(docs_seq[doc_seq_name],
                          key=lambda k: k["document_index"])
            for i, doc in enumerate(docs):
                _doc = Document.objects.filter(
                    audio_filename=doc["audio_filename"], dataset=dataset)
                if not _doc.count():
                    Document.objects.create(
                        text=doc["text"],
                        audio_filename=doc["audio_filename"],
                        sequence_index=i,
                        document_sequence=document_sequence,
                        dataset=dataset,
                        audio_duration=doc["duration"]
                    )

        # Should trigger the signal
        #dataset.is_streamed = strtobool(options["is_streamed"])
        dataset.save()
        dataset, dataset_created = Dataset.objects.filter(id=dataset.id).update(is_streamed=True)