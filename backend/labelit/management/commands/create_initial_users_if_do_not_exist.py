from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# make_password(password, salt=None, hasher='default')[source]¶


class Command(BaseCommand):
    help = 'Creates initial users for a local installation'

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
        User = get_user_model()
        
        if User.objects.filter(email="admin@labelit.com").count() > 0:
            print("Initial users exist, skipping.")
            return

        print("Creating initial users: supseruser, QA user and two annotator users...")

        User.objects.create_superuser(
            'admin',
            'admin@labelit.com',
            'adminpassword'
        )
        
        User.objects.create(
            username="QAUser",
            first_name="QA1",
            last_name="Gautier",
            is_staff=True,
            email="qa@qa.com",
            password=make_password("QApassword"),
        )

        
        User.objects.create(
            username="Annotator1",
            first_name="Annotator1",
            last_name="Smith",
            is_staff=False,
            email="a1@annotator.com",
            password=make_password("a1password"),
        )

        User.objects.create(
            username="Annotator2",
            first_name="Annotator2",
            last_name="Kim",
            is_staff=False,
            email="a2@annotator.com",
            password=make_password("a2password"),
        )
        print("Done creating users.")
        
        
        
        
