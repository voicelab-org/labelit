from django.core.management.base import BaseCommand
from labelit.models import Document, DocumentSequence, Dataset

LOREMIPSUM = "Lorem ipsum dolor sit amet. Est animi exercitationem aut tempora sunt 33 facere enim et nemo dolor sed sunt dolor cum nihil rerum? Cum consequatur temporibus eos sint blanditiis ex dicta incidunt qui illum officia rem animi nesciunt et dolores ipsa? Sit aperiam ducimus sit quas consequatur id voluptatibus earum a veritatis quia! Qui culpa porro non accusantium unde et nulla blanditiis.\r\n\rLorem ipsum dolor sit amet. Est animi exercitationem aut tempora sunt 33 facere enim et nemo dolor sed sunt dolor cum nihil rerum? Cum consequatur temporibus eos sint blanditiis ex dicta incidunt qui illum officia rem animi nesciunt et dolores ipsa? Sit aperiam ducimus sit quas consequatur id voluptatibus earum a veritatis quia! Qui culpa porro non accusantium unde et nulla blanditiis.\r\n\rLorem ipsum dolor sit amet. Est animi exercitationem aut tempora sunt 33 facere enim et nemo dolor sed sunt dolor cum nihil rerum? Cum consequatur temporibus eos sint blanditiis ex dicta incidunt qui illum officia rem animi nesciunt et dolores ipsa? Sit aperiam ducimus sit quas consequatur id voluptatibus earum a veritatis quia! Qui culpa porro non accusantium unde et nulla blanditiis.\r\n\rLorem ipsum dolor sit amet. Est animi exercitationem aut tempora sunt 33 facere enim et nemo dolor sed sunt dolor cum nihil rerum? Cum consequatur temporibus eos sint blanditiis ex dicta incidunt qui illum officia rem animi nesciunt et dolores ipsa? Sit aperiam ducimus sit quas consequatur id voluptatibus earum a veritatis quia! Qui culpa porro non accusantium unde et nulla blanditiis."


class Command(BaseCommand):
    help = "Load data from AWS S3 bucket into the database."

    def add_arguments(self, parser):

        parser.add_argument(
            "--name",
            type=str,
            required=True,
            help="Name of the dataset to be created",
        )

    def handle(self, *args, **options):
        dataset = Dataset.objects.create(name=options["name"])
        for i in range(100):
            txt = str(i) + " " + LOREMIPSUM
            Document.objects.create(
                dataset=dataset,
                text=txt,
                audio_duration=1,
            )
