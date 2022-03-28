from django.core.management.base import BaseCommand
from labelit.models import TimedTranscript, TimedTranscriptSegment
import os
import json

class Command(BaseCommand):
    help = 'Creates a TimedTranscript from a json representation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--json',
            type=str,
            default='/code/labelit/management/commands/call.json',
            dest="json",
            help="Path to .json"
        )

    def handle(self, *args, **options):
        with open(options['json'], 'r') as f:
            d = json.load(f)
            t = TimedTranscript.objects.create()
            for s in d:
                TimedTranscriptSegment.objects.create(
                    timed_transcript=t,
                    transcript=s['transcript'],
                    start_time=s['start_time']
                )