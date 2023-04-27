from django.db import models
from django.db.models.signals import pre_save
from labelit.utils.audio_utils import generate_waveform_for_dataset
from django.db.models import JSONField
from django.core.serializers.json import DjangoJSONEncoder


class Dataset(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    metadata = JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<Dataset: {} {}>".format(self.pk, self.name)


def validate_order(sender, instance, **kwargs):
    generate_waveform_for_dataset(instance.name)


pre_save.connect(validate_order, sender=Dataset)
