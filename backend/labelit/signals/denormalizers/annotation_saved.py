from labelit.models import (
    Label,
    Annotation,
    CompletedDocumentAnnotatorPair,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Annotation)
def annotation_saved(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    instance.batch.get_batch_unit(
        instance.document
    ).update_annotation_progress_statistics(saved_annotation=instance)

    # if annotator is done, create CompletedDocumentAnnotatorPair if does not exist
    done_annotations_on_doc_by_annotator = Annotation.objects.filter(
        annotator=instance.annotator,
        document=instance.document,
        batch=instance.batch,
        is_done=True,
    )

    if instance.is_done:
        if (
            done_annotations_on_doc_by_annotator.count()
            == instance.batch.project.tasks.all().count()
        ):
            try:
                CompletedDocumentAnnotatorPair.objects.get(
                    annotator=instance.annotator,
                    document=instance.document,
                    batch=instance.batch,
                    project=instance.batch.project,
                )
            except ObjectDoesNotExist:
                try:
                    CompletedDocumentAnnotatorPair.objects.create(
                        annotator=instance.annotator,
                        document=instance.document,
                        batch=instance.batch,
                        project=instance.batch.project,
                        annotation_time=instance.time,
                    )
                except IntegrityError:
                    logger.info(
                        "CompletedDocumentAnnotatorPair already exists, skipping creation"
                    )
