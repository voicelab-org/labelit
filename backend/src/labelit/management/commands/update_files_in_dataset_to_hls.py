from django.core.management.base import BaseCommand

from labelit.models import Dataset
from distutils.util import strtobool


import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Converts all files in a dataset to hls"

    def add_arguments(self, parser):
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
        dataset = Dataset.objects.get(name=options["dataset_name"])
        # Should trigger the signal
        dataset.is_streamed = strtobool(options["is_streamed"])
        dataset.save()
