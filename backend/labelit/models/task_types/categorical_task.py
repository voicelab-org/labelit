from django.db import models
from labelit.models.task import Task
from labelit.models.annotation import Annotation
from django.core.exceptions import ValidationError
from django.http import Http404
from statsmodels.stats.inter_rater import fleiss_kappa
import math
from django.db.models import F


class CategoricalTask(Task):

    are_categories_exclusive = models.BooleanField(
        """
        If true, the annotator cannot select more than one category.
        """,
        default=True,
    )

    class Meta:
        app_label = 'labelit'

    def __str__(self):
        return "<CategoricalTask ({}): {}>".format(self.pk, self.name)

    def validate_labels(
            self,
            labels,
            is_final
    ):
        if is_final:
            if len(labels) == 0:
                raise ValidationError(
                    """
                    Label required
                    """
                )
        if self.are_categories_exclusive:
            if len(labels) > 1:
                raise ValidationError(
                    """
                    `are_categories_exclusive` is set to true:
                    there can only be one categorical label per annotation
                    """
                )

    def _get_stats(self, done_annotations, annotators):
        stats = {}

        stats['annotation_distribution'] = done_annotations.values('labels__name', 'labels__color').order_by(
            'labels__name').annotate(
            count=models.Count('id')
        )

        stats['per_annotator_distributions'] = []

        for annotator in annotators:
            if done_annotations.filter(annotator=annotator).count():
                stats['per_annotator_distributions'].append(
                    done_annotations.filter(annotator=annotator).values('labels__name', 'labels__color').order_by(
                        'labels__name').annotate(
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
        stats = self._get_stats(done_annotations, annotators)
        """
        stats = {}
        try:
            stats['agreement'] = self.get_agreement_stats(batch)
        except Http404:
            stats['agreement'] = None

        

        stats['annotation_distribution'] = done_annotations.values('labels__name', 'labels__color').order_by('labels__name').annotate(
            count=models.Count('id')
        )

        stats['per_annotator_distributions'] = []

        for annotator in batch.annotators.all():
            if done_annotations.filter(annotator=annotator).count():
                stats['per_annotator_distributions'].append(
                    done_annotations.filter(annotator=annotator).values('labels__name', 'labels__color').order_by('labels__name').annotate(
                        count=models.Count('id'),
                        annotator_first_name=F('annotator__first_name'),
                        annotator_last_name=F('annotator__last_name'),
                    )
                )
                


        """
        try:
            stats['agreement'] = self.get_agreement_stats(batch)
        except Http404:
            stats['agreement'] = None

        return stats

    def get_agreement_stats(self, batch):
        if not self.are_categories_exclusive:
            raise NotImplementedError(
                """
                `are_categories_exclusive` is set to false:
                agreement stats not implemented.
                """
            )
        all_doc_stats = batch.annotations.filter(
            is_done=True,
            task=self,
        ).values('document_id').annotate(
            num_annotations_in_doc=models.Count('id')
        ).filter(
            num_annotations_in_doc=batch.num_annotators_per_document,
        )

        if all_doc_stats.count() == 0:
            raise Http404

        for label in self.labels.all():
            all_doc_stats = all_doc_stats.annotate(
                **{
                    'num_with_label_{}'.format(label.pk): models.Count(
                        'labels',
                        filter=models.Q(
                            **{
                                'labels__in': [label]
                            }
                        )
                    )
                }
            )

        M = []
        categories = [k for k in all_doc_stats[0].keys() if 'num_with_label' in k]
        categories.sort()
        for doc_stats in all_doc_stats:
            row = []
            for category in categories:
                row.append(
                    doc_stats[category]
                )
            M.append(row)

        kappa = fleiss_kappa(M, method='fleiss')

        if math.isnan(kappa):  # can happen e.g. when a single doc has been annotated so far
            raise Http404

        return {
            "metric": "Fleiss Kappa",
            "value": kappa,
        }
