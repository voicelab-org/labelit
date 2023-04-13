from django.db import models
from labelit.models.task import Task
from django.core.exceptions import ValidationError
from labelit.models.annotation import Annotation
from django.http import Http404


class NestedCategoricalTask(Task):
    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<NestedCategoricalTask ({}): {}>".format(self.pk, self.name)

    single_select = models.BooleanField(
        """
        If true, the annotator cannot select more than one label.
        """,
        default=True,
    )

    def validate_labels(self, labels, is_final):
        if len(list(filter(lambda l: l.parent_label == None, labels))) > 0:
            raise ValidationError(
                """
                Cannot select parent label, all selected labels must be children labels
                """
            )
        if is_final:
            if len(labels) == 0:
                raise ValidationError(
                    """
                    Label required
                    """
                )
        if self.single_select:
            if len(labels) > 1:
                raise ValidationError(
                    """
                    `single_select` is set to true:
                    there can only be one label per annotation
                    """
                )

    def _get_stats(
        self,
        done_annotations,
    ):
        stats = {}
        stats["children_label_distribution"] = (
            done_annotations.values("labels__name", "labels__color")
            .order_by("labels__name")
            .annotate(count=models.Count("id"))
        )
        stats["parent_label_distribution"] = (
            done_annotations.values(
                "labels__nestedcategoricallabel__parent_label__name",
                "labels__nestedcategoricallabel__parent_label__color",
            )
            .order_by("labels__nestedcategoricallabel__parent_label__name")
            .annotate(count=models.Count("id"))
        )

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
        # raise NotImplementedError
        raise Http404
