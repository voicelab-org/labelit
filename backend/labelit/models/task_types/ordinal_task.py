from django.core.exceptions import ValidationError
from django.db import models
from django.http import Http404
from labelit.utils.agreement_metrics.ordinal_alpha import OrdinalAlphaMetric
from labelit.models import Annotation, Task


class OrdinalTask(Task):
    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<OrdinalTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(
            self,
            labels,
            is_final,
    ):
        if is_final:
            if len(labels) == 0:
                raise ValidationError(
                    """
                    Label required
                    """
                )
        if len(labels) > 1:
            raise ValidationError(
                """
                there can only be one ordinal label
                """
            )

    def _get_stats(self, done_annotations, annotators):
        stats = {}

        stats['annotation_distribution'] = done_annotations.values(
            'labels__name', 'labels__color',
        ).order_by('labels__name').annotate(count=models.Count('id'))

        stats['per_annotator_distributions'] = []

        for annotator in annotators:
            if done_annotations.filter(annotator=annotator).count():
                stats['per_annotator_distributions'].append(
                    done_annotations.filter(annotator=annotator).values('labels__name', 'labels__color').order_by(
                        'labels__name').annotate(
                        count=models.Count('id'),
                        annotator_first_name=models.F('annotator__first_name'),
                        annotator_last_name=models.F('annotator__last_name'),
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

        stats = self._get_stats(done_annotations, batch.annotators.all())

        try:
            stats['agreement'] = self.get_agreement_stats(batch)
        except Http404:
            stats['agreement'] = None

        """
        stats['annotation_distribution'] = done_annotations.values('labels__name', 'labels__color',).order_by('labels__name').annotate(count=models.Count('id'))

        stats['per_annotator_distributions'] = []

        for annotator in batch.annotators.all():
            if done_annotations.filter(annotator=annotator).count():
                stats['per_annotator_distributions'].append(
                    done_annotations.filter(annotator=annotator).values('labels__name', 'labels__color').order_by('labels__name').annotate(
                        count=models.Count('id'),
                        annotator_first_name=models.F('annotator__first_name'),
                        annotator_last_name=models.F('annotator__last_name'),
                    )
                )
        """

        return stats

    def get_agreement_stats(self, batch):
        # TODO: make DRY, replicated code with CategoricalTask
        all_complete_annotations = batch.annotations.filter(
            is_done=True,
            task=self,
        ).values('document_id').annotate(
            num_annotations_in_doc=models.Count('id')
        ).filter(
            num_annotations_in_doc=batch.num_annotators_per_document,
        )

        if all_complete_annotations.count() == 0:
            raise Http404
        # END Todo

        metric = OrdinalAlphaMetric(
            num_labels=self.labels.all().count(),
        )

        alpha = metric.ordinal_krippendorff_alpha(
            metric.format_annotations_queryset(
                Annotation.objects.filter(
                    document_id__in=all_complete_annotations.values('document_id'),
                    task=self,
                    batch=batch,
                )
            )
        )

        return {
            "metric": "Weighted Krippendorff's alpha",
            "value": alpha,
        }

