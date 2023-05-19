from django.db import models
from labelit.models.sampler import Sampler
from labelit.models.document import Document
from typing import Union, List
from django.db.models import QuerySet


class SortedSampler(Sampler):
    sorting_key = models.TextField(
        "The key to sort documents by",
    )
    is_ascending = models.BooleanField(
        "Whether sorting is ascending",
        default=True,
    )

    def sample(
            self,
            documents: Union[QuerySet, List[Document]],
            target_num_documents: int
    ):
        return documents.order_by(f'{"-" if not self.is_ascending else ""}{self.sorting_key}')[:target_num_documents]

    class Meta:
        app_label = "labelit"

    def __str__(self):
        return "<SortedSampler ({}): project {}>".format(self.pk, self.project.name)
