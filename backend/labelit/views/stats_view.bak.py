from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from labelit.models.annotation import Annotation
from labelit.models.task import Task
from django.db.models.functions import TruncDate
from django.db.models import (
    Case, When, Value, IntegerField, F, Count, Sum, Subquery,
    OuterRef, Avg,
    FloatField,
)
from datetime import datetime
from datetime import timedelta
from django.db.models.functions import Cast
from labelit.utils.date_utils import ISO_string_from_date, date_from_string


class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        def _get_stats(
                min_date='2021-08-01',
                max_date='2021-12-31',
                projects=[],
                annotators=[],
        ):
            num_annotations_done_by_annotator_on_doc = Subquery(
                Annotation.objects.filter(
                    annotator=OuterRef('annotator'),
                    document=OuterRef('document')
                ).values('annotator').annotate(
                    count=Count('pk')
                ).values('count')[:1],
                output_field=IntegerField()
            )

            num_tasks = Subquery(
                Task.objects.filter(
                    projects=OuterRef('project'),
                ).values('projects').annotate(
                    count=Count('pk')
                ).values('count')[:1],
                output_field=IntegerField()
            )

            max_date += timedelta(days=1)

            done_annotations = Annotation.objects.filter(
                is_done=True,
                updated_at__gte=min_date,
                updated_at__lte=max_date,
            )

            if len(projects):
                done_annotations = done_annotations.filter(
                    project_id__in=projects
                )

            if len(annotators):
                done_annotations = done_annotations.filter(
                    annotator_id__in=annotators
                )

            completed_document_annotator_pairs = done_annotations.values(
                'document',
                'document__audio_duration',
                'annotator',
            ).annotate(
                num_done=num_annotations_done_by_annotator_on_doc,
                num_tasks=num_tasks,
                annotation_time=Avg('time')
            ).distinct().filter(num_done=F('num_tasks'))

            # total number of annotated docs over period (docs are counted
            # multiple times when there are multiple annotators)
            num_docs = completed_document_annotator_pairs.count()

            # number of annotated docs per annotator over period
            stats_per_annotator = list(completed_document_annotator_pairs.values(
                'annotator'
            ).annotate(
                num_docs=Count('document', distinct=True),
            ).values(
                'annotator',
                'annotator__first_name',
                'annotator__last_name',
                'num_docs',
            ))
            
            def _add_timing_stats(
                    document_annotator_pairs,
                    stats,
                    by_day=False
            ):
                timing_stats = []
                for pair in document_annotator_pairs:
                    if by_day:
                        filtered = list(filter(
                            lambda x: (
                                    x['annotator'] == pair['annotator'] and 
                                    x['day'] == pair['day']
                            ),
                            timing_stats
                        ))
                    else:
                        filtered = list(filter(
                            lambda x: x['annotator'] == pair['annotator'],
                            timing_stats
                        ))
                    if not len(filtered):
                        to_append = {
                            'annotator': pair['annotator'],
                            'total_duration': pair['document__audio_duration'],
                            'total_annotation_time': pair['annotation_time']
                        }
                        if by_day:
                            to_append['day'] = pair['day']
                        timing_stats.append(to_append)
                    else:
                        if pair['document__audio_duration']:
                            filtered[0]['total_duration'] += pair['document__audio_duration']
                            filtered[0]['total_annotation_time'] += pair['annotation_time']

                for stat in stats:
                    if by_day:
                        stat['total_duration'] = list(
                            filter(lambda x: (
                                x['annotator'] == stat['annotator']
                                and x['day'] == stat['day']
                            ), timing_stats)
                        )[0]['total_duration']
                        stat['total_annotation_time'] = list(
                            filter(lambda x: (
                                x['annotator'] == stat['annotator']
                                and x['day'] == stat['day']
                            ), timing_stats)
                        )[0]['total_annotation_time']
                    else:
                        stat['total_duration'] = list(
                            filter(lambda x: x['annotator'] == stat['annotator'], timing_stats)
                        )[0]['total_duration']
                        stat['total_annotation_time'] = list(
                            filter(lambda x: x['annotator'] == stat['annotator'], timing_stats)
                        )[0]['total_annotation_time']
            
            _add_timing_stats(completed_document_annotator_pairs, stats_per_annotator)
            
            total_duration = sum([s['total_duration'] for s in stats_per_annotator])

            # number of annotated docs per annotator per day over period
            completed_document_annotator_pairs_per_day = done_annotations.annotate(
                day=TruncDate(F('updated_at'))
            ).values(
                'document__audio_duration',
                'document',
                'annotator',
                'day',
            ).annotate(
                num_done=num_annotations_done_by_annotator_on_doc,
                num_tasks=num_tasks,
                annotation_time=Avg('time')
            ).distinct().filter(num_done=F('num_tasks'))

            stats_per_annotator_per_day = list(completed_document_annotator_pairs_per_day.values(
                'annotator', 'day',
            ).annotate(num_docs=Count('document', distinct=True)).values(
                'annotator',
                'annotator__first_name',
                'annotator__last_name',
                'num_docs',
                'day'
            ))

            _add_timing_stats(completed_document_annotator_pairs_per_day, stats_per_annotator_per_day, by_day=True)

            for stat in stats_per_annotator_per_day:
                stat['day'] = ISO_string_from_date(stat['day'])

            # get the total time spent annotating

            return Response({
                "num_docs": num_docs,
                "total_duration": total_duration,
                "stats_per_annotator": stats_per_annotator,
                "stats_per_annotator_per_day": stats_per_annotator_per_day
            })

        def query_param_string_to_list_int(query_param_string):
            return [int(x) for x in query_param_string.split(',') if x.strip().isdigit()]

        # get the filters
        # pass them to get_stats
        kwargs = {}

        for key in ['min_date', 'max_date', 'projects', 'annotators']:
            if key in request.GET:
                if key in ['min_date', 'max_date']:
                    kwargs[key] = date_from_string(request.GET[key])
                if key in ['projects', 'annotators']:
                    kwargs[key] = query_param_string_to_list_int(request.GET[key])

        return _get_stats(**kwargs)
