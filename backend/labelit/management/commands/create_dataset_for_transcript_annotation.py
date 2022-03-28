from django.core.management.base import BaseCommand
import json
from distutils.util import strtobool
from labelit.models import Document, DocumentSequence, Dataset


class Command(BaseCommand):
    help = "Creates a dataset from JSON file for transcript annotation"

    def add_arguments(self, parser):

        parser.add_argument(
            "--json-path",
            type=str,
            required=True,
            dest="json_file",
            help="JSON file contains dataset info",
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

        dataset, dataset_created = Dataset.objects.get_or_create(
            name=options["dataset_name"]
        )

        with open(options["json_file"], "r") as f:
            data = json.load(f)

        for key in data:
            text = data[key].replace("\n", "<br/>")
            Document.objects.create(
                text=text,
                audio_filename=key,
                audio_duration=1,
                dataset=dataset,
            )

        # Should trigger the signal
        dataset.is_streamed = strtobool(options["is_streamed"])
        dataset.save()
