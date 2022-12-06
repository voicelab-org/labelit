from django.db import models
from labelit.models.task import Task
from labelit.models.annotation import Annotation
from django.core.exceptions import ValidationError
from django.http import Http404
from statsmodels.stats.inter_rater import fleiss_kappa
import math
from django.db.models import F


class EntityTask(Task):
    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<EntityTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(
            self,
            labels,
            is_final
    ):
        pass

    def _get_stats(self, done_annotations, annotators):
        stats = {}


        stats['annotation_distribution'] = done_annotations.values(
            'labels__name',
            'labels__color'
        ).order_by('labels__name').annotate(
            count=models.Count('id')
        )

        stats['per_annotator_distributions'] = []

        for annotator in annotators:
            if done_annotations.filter(annotator=annotator).count():
                stats['per_annotator_distributions'].append(
                    done_annotations.filter(annotator=annotator).values(
                        'labels__name',
                        'labels__color'
                    ).order_by('labels__name').annotate(
                        count=models.Count('id'),
                        annotator_first_name=F('annotator__first_name'),
                        annotator_last_name=F('annotator__last_name'),
                    )
                )

        return stats

    def get_project_stats(self, project):
        done_annotations = Annotation.objects.filter(
            project=project,
            task=self,
            is_done=True,
        )
        annotators = []
        for batch in project.batches.all():
            for a in batch.annotators.all():
                annotators.append(a)
        annotators = list(set(annotators))

        return self._get_stats(done_annotations, annotators)

    def get_batch_stats(self, batch):

        done_annotations = Annotation.objects.filter(
            batch=batch,
            task=self,
            is_done=True,
        )
        annotators = batch.annotators.all()

        """

        stats['annotation_distribution'] = done_annotations.values(
            'labels__name',
            'labels__color'
        ).order_by('labels__name').annotate(
            count=models.Count('id')
        )

        stats['per_annotator_distributions'] = []

        for annotator in batch.annotators.all():
            if done_annotations.filter(annotator=annotator).count():
                stats['per_annotator_distributions'].append(
                    done_annotations.filter(annotator=annotator).values(
                        'labels__name',
                        'labels__color'
                    ).order_by('labels__name').annotate(
                        count=models.Count('id'),
                        annotator_first_name=F('annotator__first_name'),
                        annotator_last_name=F('annotator__last_name'),
                    )
                )
        """

        return self._get_stats(done_annotations, annotators)

    def get_agreement_stats(self, batch):
        #  raise NotImplementedError
        raise Http404
