from django.test import TestCase
from labelit.models import Task, CategoricalTask, OrdinalTask, Project
from labelit.serializers import ProjectWithStatsSerializer
from labelit.tests import TestSetup


class ProjectWithStatsSerializerTests(TestSetup, TestCase):
    def setUp(self):
        super().setUp()
        self.serializer1 = ProjectWithStatsSerializer(instance=self.project)

    def test_contains_expected_fields(self):
        data = self.serializer1.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "name",
                    "is_audio_annotated",
                    "is_text_annotated",
                    "are_sequences_annotated",
                    "tasks",
                    "timer_inactivity_threshold",
                    "num_done_batches",
                    "num_done_documents",
                    "num_documents",
                    "do_display_timer_time",
                    "archived",
                    "target_num_documents",
                    "target_deadline",
                    "description",
                    "does_audio_playing_count_as_activity",
                    "enable_region_annotation",
                ]
            ),
        )
