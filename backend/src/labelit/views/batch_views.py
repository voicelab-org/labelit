from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

from labelit.serializers import (
    BatchPolymorphicSerializer,
    DocumentSerializer,
    AnnotationSerializer,
    AnnotationWithUserSerializer,
    FlatBatchSerializer,
    TaskPolymorphicSerializer,
    SimpleBatchSerializer,
    AnnotationWithLabelsSerializer,
)
from labelit.models import Batch, Annotation, ProjectTask


class AnnotationsExporterPagination(PageNumberPagination):
    page_size = 250
    page_size_query_param = "page_size"


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_action_classes = {
        "create": FlatBatchSerializer,
        "list": SimpleBatchSerializer,
    }
    serializer_class = BatchPolymorphicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Batch.objects.all()
        else:
            queryset = Batch.objects.filter(annotators__id=self.request.user.id)
        project_id = self.request.query_params.get("project_id", None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @action(detail=True, name="Get progress stats for the batch")
    def get_progress(self, request, pk=None):
        batch = Batch.objects.get(pk=pk)
        data = {
            "num_done_units": batch.get_num_done_units(),
            "total": batch.get_total_units(),
        }
        return Response(data)

    @action(detail=True, name="Get number of documents to review")
    def get_num_to_review(self, request, pk=None):
        batch = Batch.objects.get(pk=pk)
        to_review_annotations = Annotation.objects.filter(
            annotator=request.user,
            batch=batch,
            has_qa_invalidated=True,
            is_resubmitted=False,
        )
        return Response({"count": to_review_annotations.count()})

    @action(detail=True, name="Get next document to review")
    def get_next_document_to_review(self, request, pk=None):
        batch = Batch.objects.get(pk=pk)
        document = batch.get_next_document_to_review(request.user)
        if document is None:
            return Response()

        annotations = []
        for task in batch.project.tasks.all():
            try:
                annotations.append(
                    Annotation.objects.get(
                        annotator=request.user,
                        document=document,
                        task=task,
                        batch=batch,
                    )
                )
            except ObjectDoesNotExist:
                return Response()

        data = {
            "document": DocumentSerializer(instance=document).data,
            "annotations": [AnnotationSerializer(instance=a).data for a in annotations],
        }
        return Response(data)

    @action(detail=True, name="Get next document to QA")
    def get_next_document_to_qa(self, request, pk=None):
        if request.GET["only_non_reviewed_annotations"] == "false":
            only_non_reviewed_annotations = False
        else:
            only_non_reviewed_annotations = True

        batch = Batch.objects.get(pk=pk)
        skip_doc_ids = []
        try:
            skip_doc_ids = [
                int(i) for i in request.GET["skipped_document_ids"].split(",")
            ]
        except:
            pass

        if only_non_reviewed_annotations:
            document = batch.get_next_document_to_qa(skipped_document_ids=skip_doc_ids)
            if document is None:
                return Response()
        else:
            document = batch.get_next_done_document(index=request.GET["index"])
            if document is None:
                return Response()

        annotations = []
        for task in batch.project.tasks.all():
            annotations += list(
                Annotation.objects.filter(
                    document=document,
                    task=task,
                    batch=batch,
                )
            )

        data = {
            "document": DocumentSerializer(instance=document).data,
            "annotations": [
                AnnotationWithUserSerializer(instance=a).data for a in annotations
            ],
            "tasks": [
                TaskPolymorphicSerializer(instance=t).data
                for t in batch.project.tasks.all()
            ],
        }
        return Response(data)

    @action(detail=True, name="Get next document to annotate for user")
    def get_next_document_to_annotate(self, request, pk=None):
        batch = Batch.objects.get(pk=pk)
        document = batch.get_next_document_to_annotate(request.user)
        if document is None:
            return Response()

        # create an annotation for each task, user
        annotations = []
        for task in batch.project.tasks.all():
            try:
                annotations.append(
                    Annotation.objects.get(
                        annotator=request.user,
                        document=document,
                        task=task,
                        batch=batch,
                    )
                )
            except ObjectDoesNotExist:
                annotations.append(
                    Annotation.objects.create(
                        annotator=request.user,
                        task=task,
                        batch=batch,
                        document=document,
                        project=batch.project,
                        document_sequence=document.document_sequence,
                    )
                )

        def _sort_annotations(annotations):
            project_tasks = ProjectTask.objects.filter(
                project_id=batch.project.id,
            )

            def _get_order(annotation):
                project_task = project_tasks.get(task=annotation.task)
                return project_task.order

            return sorted(
                annotations,
                key=_get_order,
            )

        annotations = _sort_annotations(annotations)

        data = {
            "document": DocumentSerializer(instance=document).data,
            "annotations": [AnnotationSerializer(instance=a).data for a in annotations],
        }
        return Response(data)

    @action(detail=True, name="Get last annotated document to undo annotations")
    def get_document_to_undo(self, request, pk=None):
        batch = Batch.objects.get(pk=pk)
        document = batch.get_document_to_undo(request.user)
        if document is None:
            return Response()

        annotations = []
        for task in batch.project.tasks.all():
            annotations.append(
                Annotation.objects.get(
                    annotator=request.user,
                    document=document,
                    task=task,
                    batch=batch,
                )
            )
        data = {
            "document": DocumentSerializer(instance=document).data,
            "annotations": [AnnotationSerializer(instance=a).data for a in annotations],
        }
        return Response(data)

    @action(detail=True, name="Get number of done annotations for user")
    def get_num_done_annotations(self, request, pk=None):
        batch = Batch.objects.get(pk=pk)
        num_done = batch.get_num_done_annotations_for_user(request.user)
        data = {
            "num_done": num_done,
        }
        return Response(data)

    @action(detail=True, name="Get annotation stats for this batch")
    def get_stats(self, request, pk=None):
        batch = Batch.objects.get(pk=pk)
        return Response(batch.get_stats())

    @action(detail=True, name="Exports the annotations related to an specific batch")
    def export_annotations(self, request, *args, **kwargs):
        self.pagination_class = AnnotationsExporterPagination

        batch = self.get_object()
        queryset = Annotation.objects.filter(batch=batch).order_by("id")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AnnotationWithLabelsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AnnotationWithLabelsSerializer(queryset, many=True)
        return Response(serializer.data)
