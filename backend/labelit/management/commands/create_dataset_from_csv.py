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
            filename = row["document_sequence_filename"]
            if filename not in known_doc_seq:
                known_doc_seq.add(filename)
                docs_seq[filename] = []
            docs_seq[filename].append(
                {
                    "document_index": row["document_index"],
                    "text": row["text"],
                    "audio_filename": row["document_filename"],
                }
            )
        for doc_seq in docs_seq:
            document_sequence, created = DocumentSequence.objects.get_or_create(
                name=doc_seq, dataset=dataset
            )
            docs = sorted(docs_seq[doc_seq], key=lambda k: k["document_index"])
            for i, doc in enumerate(docs):
                Document.objects.create(
                    text=doc["text"],
                    audio_filename=doc["audio_filename"],
                    sequence_index=i,
                    document_sequence=document_sequence,
                    dataset=dataset,
                )

        # Should trigger the signal
        dataset.is_streamed = strtobool(options["is_streamed"])
        dataset.save()