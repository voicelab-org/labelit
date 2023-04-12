from labelit.models import Task
from django.db import models
from zope.dottedname.resolve import resolve


class RealtimeVideoDimensionalTask(Task):
    validator = models.CharField(
        "Dotted path to the validator class",
        max_length=500,
        default="labelit.validators.base_realtime_dimensional_annotation_validator.BaseRealtimeDimensionalAnnotationValidator",
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<RealtimeVideoDimensionalTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(
        self,
        labels,
        _,
    ):
        resolve(self.validator)().validate(labels[0])

    def get_agreement_stats(self, batch):
        return {}
