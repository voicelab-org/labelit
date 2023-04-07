from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from labelit.models.completed_document_annotator_pair import (
    CompletedDocumentAnnotatorPair,
)
from django.db.models.functions import TruncDate
from django.db.models import (
    Case,
    When,
    Value,
    IntegerField,
    F,
    Count,
    Sum,
    Subquery,
    OuterRef,
    Avg,
    FloatField,
)
from datetime import timedelta
from labelit.utils.date_utils import ISO_string_from_date, date_from_string


class StatsView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        def _get_stats(
            min_date="1950-08-01",
            max_date="3022-03-01",
            projects=[],
            annotators=[],
        ):
            if isinstance(max_date, str):
                max_date = date_from_string(max_date)
                min_date = date_from_string(min_date)

            max_date += timedelta(days=1)

            completed_document_annotator_pairs = (
                CompletedDocumentAnnotatorPair.objects.filter(
                    created_at__gte=min_date,
                    created_at__lte=max_date,
                )
            )

            if len(projects):
                completed_document_annotator_pairs = (
                    completed_document_annotator_pairs.filter(project_id__in=projects)
                )

            if len(annotators):
                completed_document_annotator_pairs = (
                    completed_document_annotator_pairs.filter(
                        annotator_id__in=annotators
                    )
                )

            if completed_document_annotator_pairs.count() == 0:
                return Response(
                    {
                        "num_docs": 0,
                        "total_duration": 0,
                        "total_duration": 0,
                        "stats_per_annotator": [],
                        "stats_per_annotator_per_day": [],
                    }
                )

            num_docs = completed_document_annotator_pairs.count()

            # number of annotated docs per annotator over period
            stats_per_annotator = list(
                completed_document_annotator_pairs.values("annotator")
                .annotate(
                    num_docs=Count("document"),
                    total_duration=Sum("document__audio_duration"),
                    time_spent=Sum("annotation_time"),
                )
                .values(
                    "annotator",
                    "annotator__first_name",
                    "annotator__last_name",
                    "num_docs",
                    "total_duration",
                    "time_spent",
                )
            )

            # number of annotated docs per annotator per day over period
            completed_document_annotator_pairs_per_day = (
                completed_document_annotator_pairs.annotate(
                    day=TruncDate(F("created_at"))
                )
            )

            stats_per_annotator_per_day = list(
                completed_document_annotator_pairs_per_day.values(
                    "annotator",
                    "day",
                )
                .annotate(
                    num_docs=Count("document", distinct=True),
                    total_duration=Sum("document__audio_duration"),
                    time_spent=Sum("annotation_time"),
                )
                .values(
                    "annotator",
                    "annotator__first_name",
                    "annotator__last_name",
                    "num_docs",
                    "total_duration",
                    "time_spent",
                    "day",
                )
            )

            for stat in stats_per_annotator_per_day:
                stat["day"] = ISO_string_from_date(stat["day"])

            # get the total time spent annotating

            return Response(
                {
                    "num_docs": num_docs,
                    "total_duration": 0,
                    "stats_per_annotator": stats_per_annotator,
                    "stats_per_annotator_per_day": stats_per_annotator_per_day,
                }
            )

        def query_param_string_to_list_int(query_param_string):
            return [
                int(x) for x in query_param_string.split(",") if x.strip().isdigit()
            ]

        # get the filters
        # pass them to get_stats
        kwargs = {}

        for key in ["min_date", "max_date", "projects", "annotators"]:
            if key in request.GET:
                if key in ["min_date", "max_date"]:
                    kwargs[key] = date_from_string(request.GET[key])
                if key in ["projects", "annotators"]:
                    kwargs[key] = query_param_string_to_list_int(request.GET[key])

        return _get_stats(**kwargs)
