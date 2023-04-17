from django.db import models
from django.conf import settings
from polymorphic.models import PolymorphicModel
from .batch_document import BatchDocument
from .annotation import Annotation
from .document import Document
import math
from django.db.models import Avg, F, ExpressionWrapper, FloatField, Count
from django.db.models.functions import Cast
from psycopg2.errors import DivisionByZero
import logging

logger = logging.getLogger(__name__)

class Batch(PolymorphicModel):
    name = models.CharField("The name of the batch", max_length=200)
    dataset = models.ForeignKey("labelit.Dataset", on_delete=models.CASCADE)
    project = models.ForeignKey(
        "labelit.Project",
        on_delete=models.CASCADE,
        related_name="batches",
    )
    annotators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )
    documents = models.ManyToManyField(
        "labelit.Document", related_name="batches", through="labelit.BatchDocument"
    )
    num_annotators_per_document = models.IntegerField(
        "The target number of annotators per document", default=1
    )
    archived = models.BooleanField(
        default=False,
    )
    # BEGIN annotation mode
    ALL_YOU_CAN_ANNOTATE = "all_you_can_annotate"
    EVEN = "even"  # consider renaming > "equal"
    ANNOTATION_MODES = [
        (
            ALL_YOU_CAN_ANNOTATE,
            """ 
            Annotators can annotate as much they want (up to optional limit)
            By the end of the batch, annotators may have done unequal amounts
            of work.
            """,
        ),
        (
            EVEN,
            """
            By the end of the batch, every annotator will have annotated
            the same number of documents
            """,
        ),
    ]
    annotation_mode = models.CharField(
        max_length=32,
        choices=ANNOTATION_MODES,
        default=EVEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # END annotation mode
    annotation_limit = models.IntegerField(
        """
        Maximum number of annotated documents per user in this batch.
        """,
        null=True,
        blank=True,
    )
    # BEGIN denormalized fields
    num_documents = models.IntegerField(
        "The number of documents in this batch (denormalized field)", default=1
    )
    # END denormalized fields

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<Batch ({}): {}>".format(self.pk, self.name)

    def get_batch_unit(self, document):
        return BatchDocument.objects.get(document=document, batch=self)

    def get_stats(self):
        stats = {}
        stats["num_done"] = self.get_num_done_units()

        done_annotations = Annotation.objects.filter(
            batch=self,
            is_done=True,
        )

        stats["average_time_per_document"] = done_annotations.aggregate(
            average=Avg(F("time"))
        )

        stats["num_annotations"] = done_annotations.count()

        stats["num_to_review"] = done_annotations.filter(
            has_qa_invalidated=True,
            is_resubmitted=False,
        ).count()

        stats["num_validated"] = done_annotations.filter(
            has_qa_validated=True,
        ).count()

        stats["num_invalidated"] = done_annotations.filter(
            has_qa_invalidated=True,
        ).count()

        stats["num_qa_seen"] = stats["num_validated"] + stats["num_invalidated"]

        if self.project.is_audio_annotated:
            try:
                stats["average_ratio"] = (
                    done_annotations.values(
                        "document_id",
                    )
                    .annotate(
                        ratio=Cast(F("time"), output_field=FloatField())
                        / Cast(F("document__audio_duration"), output_field=FloatField()),
                        time=F("time"),
                        dur=F("document__audio_duration"),
                    )
                    .aggregate(average=Avg(F("ratio")))
                )
            except DivisionByZero as e:
                logger.warning(f"Cannot compute average_ratio, some documents have a duration of 0. {repr(e)}")
                stats["average_ratio"] = 0

            stats["average_duration"] = done_annotations.values(
                "document_id"
            ).aggregate(average=Avg(F("document__audio_duration")))

        stats["annotator_stats"] = []
        for annotator in self.annotators.all():
            a_stats = {
                "name": annotator.first_name + " " + annotator.last_name,
            }
            try:
                a_stats["num_documents_annotated"] = (
                    done_annotations.filter(
                        annotator=annotator,
                    )
                    .values("annotator")
                    .annotate(count=Count("document_id", distinct=True))
                    .values("count")[0]["count"]
                )
            except IndexError:
                a_stats["num_documents_annotated"] = 0

            if self.project.is_audio_annotated:
                a_stats["average_ratio"] = (
                    done_annotations.filter(
                        annotator=annotator,
                    )
                    .values(
                        "document_id",
                    )
                    .annotate(
                        ratio=Cast(F("time"), output_field=FloatField())
                        / Cast(
                            F("document__audio_duration"), output_field=FloatField()
                        ),
                        time=F("time"),
                        dur=F("document__audio_duration"),
                    )
                    .aggregate(average=Avg(F("ratio")))
                )

            stats["annotator_stats"].append(a_stats)

        return stats

    def get_annotation_limit(self):
        if self.annotation_mode == self.EVEN:
            assert self.annotation_limit is None
            limit = math.floor(
                self.num_documents
                * self.num_annotators_per_document
                / self.annotators.all().count()
            )
            if limit == 0:
                limit = 1
            return limit
        else:
            if self.annotation_limit is not None:
                return self.annotation_limit
        return math.inf

    def get_next_document_to_review(self, user):
        invalidated = (
            Annotation.objects.filter(
                batch=self,
                annotator=user,
                has_qa_invalidated=True,
                is_resubmitted=False,
            )
            .order_by("updated_at")
            .first()
        )
        if invalidated:
            return invalidated.document
        return None

    def get_next_done_document(self, index=0):
        completed_batch_docs = BatchDocument.objects.filter(
            batch=self,
            num_done_annotators=self.num_annotators_per_document,
        ).order_by("id")
        try:
            document = Document.objects.get(
                id=completed_batch_docs[int(index)].document_id
            )
            return document
        except IndexError:
            return None

    def get_next_document_to_qa(self, skipped_document_ids=[]):
        completed_batch_docs = BatchDocument.objects.filter(
            batch=self,
            num_done_annotators=self.num_annotators_per_document,
        ).exclude(document__id__in=skipped_document_ids)
        batch_annotations = Annotation.objects.filter(
            batch_id__in=completed_batch_docs.values("batch_id"),
            document_id__in=completed_batch_docs.values("document_id"),
        )
        try:
            return Document.objects.get(
                id=batch_annotations.filter(
                    is_resubmitted=True,
                    has_qa_invalidated=True,
                )
                .order_by("updated_at")
                .values("document_id")
                .first()["document_id"]
            )
        except TypeError:
            try:
                return Document.objects.get(
                    id=batch_annotations.filter(
                        is_resubmitted=False,
                        has_qa_validated=False,
                        has_qa_invalidated=False,
                    )
                    .order_by("updated_at")
                    .values("document_id")
                    .first()["document_id"]
                )
            except TypeError:
                return None

    def get_next_document_to_annotate(self, user):
        in_progress_annotations = Annotation.objects.filter(
            batch=self, annotator=user, is_done=False
        )
        if in_progress_annotations.count() > 0:
            return in_progress_annotations.first().document

        annotated_doc_ids = set(
            Annotation.objects.filter(
                batch=self,
                annotator=user,
                is_done=True,
            ).values_list("document_id")
        )

        assert not len(annotated_doc_ids) > self.get_annotation_limit()
        if len(annotated_doc_ids) >= self.get_annotation_limit():
            return None

        incomplete_batch_docs = BatchDocument.objects.filter(
            batch=self,
            num_annotators__lt=self.num_annotators_per_document,
        )
        for incomplete_batch_doc in incomplete_batch_docs:
            if (
                Annotation.objects.filter(
                    annotator=user,
                    batch=incomplete_batch_doc.batch,
                    document=incomplete_batch_doc.document,
                ).count()
                == 0
            ):
                return incomplete_batch_doc.document
        return None

    def get_num_done_units(self):
        return BatchDocument.objects.filter(
            batch=self, num_done_annotators=self.num_annotators_per_document
        ).count()

    def get_total_units(self):
        return self.num_documents

    @staticmethod
    def get_remaining_units_in_dataset(project, dataset):
        return (
            dataset.documents.all().count()
            - BatchDocument.objects.filter(
                document__dataset=dataset, batch__in=project.batches.all()
            ).count()
        )

    def get_num_done_annotations_for_user(self, user):
        done_annotations = Annotation.objects.filter(
            batch=self,
            annotator=user,
            is_done=True,
        )
        num_tasks = self.project.tasks.count()

        return done_annotations.count() // num_tasks

    def get_document_to_undo(self, user):
        doc_id = list(
            self.annotations.filter(
                is_done=True,
                annotator=user,
            )
            .values("document_id")
            .annotate(
                num_annotations_in_doc=models.Count("id"),
                last_update=models.Max("updated_at"),
            )
            .filter(num_annotations_in_doc=self.project.tasks.count())
            .order_by("-last_update")
        )[0]["document_id"]

        if doc_id is not None:
            return Document.objects.get(id=doc_id)
        else:
            return None
