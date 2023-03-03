from django.test import TestCase
from django.contrib.auth import get_user_model

from labelit.models import Batch, Project, Dataset, Document, BatchDocument
from labelit.serializers import BatchSerializer, FlatBatchSerializer
import logging

logger = logging.getLogger(__name__)


class BatchSerializerTests(TestCase):
    def setUp(self):
        self.dataset = Dataset.objects.create(
            name="IMDB reviews",
        )
        self.docs = []

        for text in ["some text", "other text", "lorem ipsum", "doloris"]:
            self.docs.append(Document.objects.create(text=text, dataset=self.dataset))
        self.project = Project.objects.create(name="Sentiment")

        self.users = []

        for u in [
            ("jane", "doe", "janedoe@labelit"),
            ("john", "doe", "johndoe@labelit"),
            ("bat", "man", "batman@labelit"),
        ]:
            self.users.append(
                get_user_model().objects.create(
                    first_name=u[0], last_name=u[1], username=u[0] + u[1], email=u[2]
                )
            )
        self.batch = Batch.objects.create(
            name="Batch 1",
            dataset=self.dataset,
            project=self.project,
            num_documents=2,
        )
        self.batch.annotators.set(self.users)
        self.batch.documents.set(self.docs[:2])
        self.serializer1 = BatchSerializer(instance=self.batch)

    def test_contains_expected_fields_and_specific_fields_and_resourcetype(self):
        self.assertEqual(
            set(self.serializer1.data.keys()),
            set(
                [
                    "id",
                    "name",
                    "dataset",
                    "project",
                    "annotators",
                    "documents",
                    "num_documents",
                    "num_annotators_per_document",
                    "annotation_mode",
                    "annotation_limit",
                ]
            ),
        )

    def test_create_batch(self):
        validated_data = dict()
        validated_data["name"] = "batch1"
        validated_data["dataset"] = self.dataset.pk
        validated_data["project"] = self.project.pk
        validated_data["annotators"] = [self.users[0].pk, self.users[1].pk]
        validated_data["num_documents"] = 2
        validated_data["num_annotators_per_document"] = 1
        validated_data["annotation_mode"] = "even"

        serializer = FlatBatchSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
        else:
            logger.error(serializer.errors)
            self.assertTrue(serializer.is_valid())

        self.assertEqual(BatchDocument.objects.filter(batch=instance).count(), 2)
