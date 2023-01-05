from django.core.management.base import BaseCommand
from labelit.models import Annotation, BatchDocument, BatchDocumentSequence


class Command(BaseCommand):
    help = 'Creates an agent user'

    def add_arguments(self, parser):
        """
        parser.add_argument(
            '--first-name',
            type=str,
            default='',
            dest="first_name",
            help="First name"
        )
        """
        pass

    def handle(self, *args, **options):
        Annotation.objects.all().delete()
        for batch_unit_cls in [BatchDocument, BatchDocumentSequence]:
            for bu in batch_unit_cls.objects.all():
                bu.num_done_annotators = 0
                bu.num_annotators = 0
                bu.save()
