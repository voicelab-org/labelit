from django.db import models
from labelit.models.task import Task
from django.core.exceptions import ValidationError


class NestedCategoricalTask(Task):

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<NestedCategoricalTask ({}): {}>".format(self.pk, self.name)

    single_select = models.BooleanField(
        """
        If true, the annotator cannot select more than one label.
        """,
        default=True,
    )

    def validate_labels(
            self,
            labels,
            is_final
    ):
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

    def _get_stats(self, done_annotations, annotators):
        raise NotImplementedError

    def get_project_stats(self, project):
        raise NotImplementedError

    def get_batch_stats(self, batch):
        raise NotImplementedError

    def get_agreement_stats(self, batch):
        raise NotImplementedError