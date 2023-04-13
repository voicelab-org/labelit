from rest_framework import serializers
from labelit.models import Task
from rest_polymorphic.serializers import PolymorphicSerializer
from .label_serializer import LabelPolymorphicSerializer
from labelit.services.polymorphic_serializer_mapping_creator import (
    create_polymorphic_serializer_mapping,
)

# from labelit.serializers.task_types import *
from zope.dottedname.resolve import resolve
from django.contrib.contenttypes.models import ContentType
import os


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


"""
def _get_mapping(
    is_create_or_update=False,
):
    def _get_dotted_paths():
        def _get_task_names():
            task_model_filenames = list(
                filter(
                    lambda fname: fname.endswith("task.py"),
                    os.listdir(
                        os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            "../models/task_types",
                        )
                    ),
                )
            )

            def _model_file_name_to_class_name(model_filename):
                return "".join(
                    map(
                        lambda name: name.capitalize(),
                        model_filename.split(".")[0].split("_"),
                    )
                )

            return list(map(_model_file_name_to_class_name, task_model_filenames))

        task_names = _get_task_names()

        return list(map(lambda name: f"labelit.models.{name}", task_names))

    task_dotted_paths = _get_dotted_paths()

    def _get_serializer_dotted_paths():
        serializer_dotted_paths = []
        corresponding_task_dotted_paths = []
        for task_dotted_path in task_dotted_paths:
            task_name = task_dotted_path.split(".")[-1]
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
        for (serializer_dotted_path, task_dotted_path) in zip(
            serializer_dotted_paths, task_dotted_paths
        )
    }
"""


create_or_update_mappping = create_polymorphic_serializer_mapping(
    is_create_or_update=True
)


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


mapping = create_polymorphic_serializer_mapping()


class TaskPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = mapping
