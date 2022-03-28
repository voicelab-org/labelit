from django.db.models.signals import m2m_changed
from labelit.models import Label, Annotation


def annotation_labels_changed(sender, **kwargs):
    action = kwargs.pop('action', None)
    instance = kwargs.pop('instance', None)
    pk_set = kwargs.pop('pk_set', None)

    instance.task.validate_labels(
        current_labels=Label.objects.filter(
            pk__in=instance.labels.values('pk')
        ),
        changed_labels=Label.objects.filter(
            pk__in=pk_set
        ),
        action=action,
        is_final=instance.is_done
    )


m2m_changed.connect(
    annotation_labels_changed,
    sender=Annotation.labels.through
)
