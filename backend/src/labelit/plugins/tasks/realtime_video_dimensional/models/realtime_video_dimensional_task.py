from django.db import models
from labelit.models.task import Task
from django.core.exceptions import ValidationError
from labelit.models.annotation import Annotation
from django.http import Http404


class RealtimeVideoDimensionalTask(Task):
    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<RealtimeVideoDimensionalTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(self, labels, is_final):
        pass  # TODO

    def _get_stats(
        self,
        done_annotations,
    ):
        stats = {}
        return stats

    def get_project_stats(self, project):
        done_annotations = Annotation.objects.filter(
            project=project,
            task=self,
            is_done=True,
        )

        return self._get_stats(done_annotations)

    def get_batch_stats(self, batch):
        done_annotations = Annotation.objects.filter(
            batch=batch,
            task=self,
            is_done=True,
        )

        return self._get_stats(done_annotations)

    def get_agreement_stats(self, batch):
        raise Http404
