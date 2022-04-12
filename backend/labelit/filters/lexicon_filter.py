import django_filters
from labelit.models import Lexicon, Project


class LexiconFilter(django_filters.FilterSet):
    projects = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Project.objects.all(),
    )

    class Meta:
        model = Lexicon
        fields = ('name', 'projects')
