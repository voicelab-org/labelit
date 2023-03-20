from rest_framework import serializers
from labelit.models import *
from rest_polymorphic.serializers import PolymorphicSerializer
from .label_serializer import LabelPolymorphicSerializer
from labelit.serializers.task_types import *
from zope.dottedname.resolve import resolve
from django.contrib.contenttypes.models import ContentType

class CreateOrUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "can_documents_be_invalidated",
            "labels",
            "archived",
        ]


def _get_mapping(
        is_create_or_update=False,
):
    def _get_dotted_paths():

        def _get_task_names():
            def _get_task_contenttype_ids():
                task_content_types = ContentType.objects.filter(
                    model__contains="task"
                ).exclude(model="task")
                return task_content_types.values_list('id', flat=True)

            task_contenttype_ids = _get_task_contenttype_ids()

            def _get_class_name(contenttype_id):
                return str(
                    ContentType.model_class(
                        ContentType.objects.get(id=contenttype_id)
                    )
                ).split("'")[1].split('.')[-1]

            return list(
                map(
                    lambda id: _get_class_name(id),
                    task_contenttype_ids,
                )
            )

        task_names = _get_task_names()

        return list(map(
            lambda name: f'labelit.models.{name}',
            task_names
        ))

    task_dotted_paths = _get_dotted_paths()

    def _get_serializer_dotted_paths():
        serializer_dotted_paths = []
        corresponding_task_dotted_paths = []
        for task_dotted_path in task_dotted_paths:
            task_name = task_dotted_path.split('.')[-1]
            if is_create_or_update:
                dotted_path = f"labelit.task_types.serializers.CreateOrUpdate{task_name}Serializer"
            else:
                dotted_path = f"labelit.task_types.serializers.{task_name}Serializer"
            try:
                resolve(dotted_path)
            except ModuleNotFoundError:
                continue
            serializer_dotted_paths.append(dotted_path)
            corresponding_task_dotted_paths.append(task_dotted_paths)
        return (serializer_dotted_paths, task_dotted_paths)

    serializer_dotted_paths, task_dotted_paths = _get_serializer_dotted_paths()

    return {
        resolve(task_dotted_path): resolve(serializer_dotted_path)
        for (serializer_dotted_path, task_dotted_path) in zip(serializer_dotted_paths, task_dotted_paths)
    }


create_or_update_mappping = _get_mapping(is_create_or_update=True)

class CreateOrUpdateTaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = create_or_update_mappping


class TaskSerializer(serializers.ModelSerializer):
    labels = LabelPolymorphicSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "projects",
            "can_documents_be_invalidated",
            "labels",
            "html_guidelines",
            "archived",
            "created_at",
            "updated_at",
        ]


mapping = _get_mapping()

class TaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = mapping