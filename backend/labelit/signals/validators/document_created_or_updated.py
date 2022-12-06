from django.db.models.signals import m2m_changed
from labelit.models import Label, Annotation, Document
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.core.exceptions import ValidationError


def _validate(document):
    if document.audio_filename is not None:
        if document.audio_duration == 0:
            raise ValidationError
    return


"""
@receiver(post_save, sender=Annotation)
def annotation_saved(sender, **kwargs):"""

@receiver(pre_save, sender=Document)
def document_saved(sender, instance, **kwargs):
    print("&SHERE", instance)
    if kwargs.get("raw", True):
        return
    # document = kwargs.pop("instance", None)
    document = instance
    _validate(document)

