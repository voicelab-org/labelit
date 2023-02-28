from rest_framework import serializers
from labelit.models import Lexicon
from .lexicon_entry_serializer import LexiconEntrySerializer


class LexiconSerializer(serializers.ModelSerializer):
    entries = LexiconEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Lexicon
        fields = [
            "id",
            "name",
            "entries",
        ]
