from rest_framework import serializers
from labelit.models import Project
from labelit.serializers import TaskPolymorphicSerializer, TaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskPolymorphicSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'is_audio_annotated',
            'is_text_annotated',
            'are_sequences_annotated',
            'tasks',
            'timer_inactivity_threshold',
            'archived',
            'do_display_timer_time',
            'does_audio_playing_count_as_activity',
        ]


class ProjectWithStatsSerializer(serializers.ModelSerializer):
    tasks = TaskPolymorphicSerializer(many=True, required=False)
    num_documents = serializers.SerializerMethodField()
    num_done_documents = serializers.SerializerMethodField()
    num_done_batches = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'is_audio_annotated',
            'is_text_annotated',
            'are_sequences_annotated',
            'tasks',
            'timer_inactivity_threshold',
            'num_documents',
            'num_done_documents',
            'num_done_batches',
            'archived',
            'target_num_documents',
            'target_deadline',
            'description',
            'do_display_timer_time',
            'does_audio_playing_count_as_activity',
        ]
        
    def get_num_documents(self, obj):
        return obj.get_num_documents()
    
    def get_num_done_documents(self, obj):
        return obj.get_num_done_documents()
    
    def get_num_done_batches(self, obj):
        return obj.get_num_done_batches()

