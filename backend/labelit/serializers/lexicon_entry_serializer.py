from rest_framework import serializers
from labelit.models import LexiconEntry


class LexiconEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LexiconEntry
        fields = [
            'id',
            'entry',
            'lexicon',
        ]
