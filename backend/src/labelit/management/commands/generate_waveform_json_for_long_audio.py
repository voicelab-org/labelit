from django.core.management.base import BaseCommand

from labelit.models import Dataset
from distutils.util import strtobool


import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "generate waveform json for long audio"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dataset-name",
            type=str,
            required=True,
            dest="dataset_name",
            help="Dataset name to be created",
        )

    def handle(self, *args, **options):
        dataset = Dataset.objects.get(name=options["dataset_name"])
        # Should trigger the signal
        dataset.save()
