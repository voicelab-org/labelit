from django.db import models
from polymorphic.models import PolymorphicModel


class Sampler(PolymorphicModel):
    project = models.OneToOneField(
        "labelit.Project",
        on_delete=models.CASCADE,
        related_name="sampler",
    )

    def sample(self, documents, target_num_documents):
        raise NotImplementedError

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<Sampler ({}): project {}>".format(self.pk, self.project.name)
