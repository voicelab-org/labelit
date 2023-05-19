from django.db import models
from labelit.models.task import Task
from labelit.models.annotation import Annotation
from django.core.exceptions import ValidationError
from statsmodels.stats.inter_rater import fleiss_kappa
import math
from django.db.models import F

from zope.dottedname.resolve import resolve


class TextEditionTask(Task):
    validator = models.CharField(
        "Dotted path to the validator class",
        max_length=500,
        default="labelit.validators.base_transcription_validator.BaseTranscriptionValidator",
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<TextEditionTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(
        self,
        labels,
        is_final,
    ):
        resolve(self.validator)().validate(labels[0].edited_text)

    def get_agreement_stats(self, batch):
        return {}
