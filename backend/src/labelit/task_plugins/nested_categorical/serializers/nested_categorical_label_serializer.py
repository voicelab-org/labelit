from rest_framework import serializers
from labelit.models import (
    NestedCategoricalLabel,
)


class NestedCategoricalLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NestedCategoricalLabel
        fields = [
            "id",
            "name",
            "task",
            "parent_label",
            "single_child_select",
        ]
