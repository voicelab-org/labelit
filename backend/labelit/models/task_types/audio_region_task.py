from django.db import models
from labelit.models.task import Task
from labelit.models.annotation import Annotation
from django.core.exceptions import ValidationError
from django.http import Http404
from statsmodels.stats.inter_rater import fleiss_kappa
import math
from django.db.models import F


class AudioRegionTask(Task):
    color = models.CharField(
        "Color for this task",
        max_length=500,
        default='blue',
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<AudioRegionTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(
            self,
            labels,
            is_final
    ):
        pass

    def _get_stats(self, done_annotations, annotators):
        raise NotImplementedError

    def get_batch_stats(self, batch):
        raise NotImplementedError

    def get_agreement_stats(self, batch):
        raise NotImplementedError
