from django.db import models
from labelit.models.sampler import Sampler
from labelit.models.document import Document
from typing import Union, List
from django.db.models import QuerySet


class ActiveSampler(Sampler):
    learner = models.FileField(upload_to="active_learning_models")

    def sample(
            self,
            documents: Union[QuerySet, List[Document]],
            target_num_documents: int
    ):
        raise NotImplementedError

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<SortedSampler ({}): project {}>".format(self.pk, self.project.name)
