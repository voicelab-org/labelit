from django.test import TestCase
from labelit.models import (
    Project,
    Dataset,
    Document,
    Batch,
    ActiveSampler,
)
from modAL.models import ActiveLearner
from modAL.uncertainty import uncertainty_sampling
from sklearn.ensemble import RandomForestClassifier
import pickle
from django.core.files import File

"""
class UploadedFile(models.Model):
  document = models.FileField(upload_to=PATH)


from django.core.files import File

doc = UploadedFile()
with open(filepath, 'rb') as doc_file:
   doc.document.save(filename, File(doc_file), save=True)
doc.save()
"""


class ActiveSamplerTests(TestCase):
    # fixtures = ["test_data"]

    def setUp(self):

        self.learner = ActiveLearner(
            estimator=RandomForestClassifier(),
            query_strategy=uncertainty_sampling
        )

        self.project = Project.objects.get(pk=6)



        self.active_sampler = ActiveSampler.objects.create(

        )
        self.documents = Document.objects.filter(pk__in=(6, 7, 8))

    def test_sample(self):
        raise NotImplementedError
