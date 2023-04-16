from labelit.models.task import Task
from labelit.models.annotation import Annotation


class EmotionCategoricalTask(Task):
    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<EmotionCategoricalTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(self, labels, is_final):
        pass  # TODO

    def _get_stats(
        self,
        done_annotations,
    ):
        stats = {}
        # TODO

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
        return {}
