from django.db import models
from .batch_document import BatchDocument
from .batch import Batch
from django.db.models import Case, When, Value, IntegerField, F, Count, Sum
from django.db import models
from .batch_document import BatchDocument
from .annotation import Annotation
from django.db.models import Avg, F, ExpressionWrapper, FloatField, Count
from django.db.models.functions import Cast
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=500)
    is_audio_annotated = models.BooleanField(default=True)
    is_text_annotated = models.BooleanField(default=True)
    enable_region_annotation = models.BooleanField(default=False)
    are_sequences_annotated = models.BooleanField(  # TODO: rename
        """
        If True: documents are presented as entire sequences with order preserved.
        If False: documents are presented one by one, in no particular order
        """,
        default=False,
    )
    timer_inactivity_threshold = models.IntegerField(
        """
        Delay (ms) past which the timer is paused during annotation
        """,
        default=60000,
    )
    do_display_timer_time = models.BooleanField(
        """
        If true, the time recorded by the timer (with inactivity pausing) will be displayed to the annotator.
        Useful for QA also.
        """,
        default=False,
    )
    does_audio_playing_count_as_activity = models.BooleanField(
        """
        If true, the timer will not pause while audio playing, even if no user interactions (mouse clicks, typing)
        occur.
        """,
        default=False,
    )
    tasks = models.ManyToManyField(
        "labelit.Task",
        related_name="projects",:
    )
    archived = models.BooleanField(
        default=False,
    )

    target_num_documents = models.IntegerField(
        "The target number of documents for this project"
    )

    target_deadline = models.DateField(
        "The target date at which we want the target number of documents to be annotated"
    )

    description = models.TextField(
        "Description of the project",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<Project ({}): {}>".format(self.pk, self.name)

    def get_num_batches(self):
        return Batch.objects.filter(project=self).count()

    def get_num_done_batches(self):
        return (
            BatchDocument.objects.filter(
                batch__in=self.batches.all(),
            )
            .annotate(
                is_done=Case(
                    When(
                        num_done_annotators=F("batch__num_annotators_per_document"),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .values(
                "batch", "batch__num_annotators_per_document", "batch__num_documents"
            )
            .annotate(num_done=Sum("is_done"))
            .filter(num_done=F("batch__num_documents"))
            .count()
        )

    def get_num_done_documents(self):
        return (
            BatchDocument.objects.filter(
                batch__in=self.batches.all(),
            )
            .annotate(
                is_done=Case(
                    When(
                        num_done_annotators=F("batch__num_annotators_per_document"),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .filter(is_done=True)
            .count()
        )

    def get_num_documents(self):
        return BatchDocument.objects.filter(
            batch__in=self.batches.all(),
        ).count()

    def get_stats(self):
        # TODO: make DRY with batch.get_stats
        stats = {}

        stats["num_done"] = sum(
            [batch.get_num_done_units() for batch in self.batches.all()]
        )

        done_annotations = Annotation.objects.filter(
            project=self,
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

        if self.is_audio_annotated:
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

            stats["average_duration"] = done_annotations.values(
                "document_id"
            ).aggregate(average=Avg(F("document__audio_duration")))

        stats["annotator_stats"] = []

        annotators = []
        for batch in self.batches.all():
            for a in batch.annotators.all():
                annotators.append(a)
        annotators = list(set(annotators))
        for annotator in annotators:
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

            if self.is_audio_annotated:
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
