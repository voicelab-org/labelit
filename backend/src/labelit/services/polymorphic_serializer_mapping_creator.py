import os
from labelit.models import *
from zope.dottedname.resolve import resolve


def create_polymorphic_serializer_mapping(
    is_create_or_update=False,
    is_task_mapping=True,
):
    if is_task_mapping:
        model_type_name = "task"
    else:
        model_type_name = "label"

    def _get_dotted_paths_with_corresponding_plugin_names():
        def _get_model_names():
            def _is_of_desired_type(model_filename):
                return model_filename.endswith(f"{model_type_name}.py")

            here = os.path.abspath(os.path.dirname(__file__))
            plugins_path = os.path.join(here, "../plugins")
            model_file_names = []
            plugin_names = []
            for plugin_name in os.listdir(plugins_path):
                if plugin_name.startswith("_"):
                    continue
                plugin_model_filenames = list(
                    filter(
                        _is_of_desired_type,
                        os.listdir(os.path.join(plugins_path, plugin_name, "models")),
                    )
                )

                model_file_names += plugin_model_filenames
                plugin_names += list(map(lambda _: plugin_name, plugin_model_filenames))

            def _model_file_name_to_class_name(model_filename):
                return "".join(
                    map(
                        lambda name: name.capitalize(),
                        model_filename.split(".")[0].split("_"),
                    )
                )

            return (
                list(map(_model_file_name_to_class_name, model_file_names)),
                plugin_names,
            )

        model_names, plugin_names = _get_model_names()

        dotted_paths = list(map(lambda name: f"labelit.models.{name}", model_names))

        return dotted_paths, plugin_names

    (
        model_dotted_paths,
        plugin_names,
    ) = _get_dotted_paths_with_corresponding_plugin_names()

    def _get_serializer_dotted_paths():
        serializer_dotted_paths = []
        corresponding_model_dotted_paths = []
        for model_dotted_path, plugin_name in zip(model_dotted_paths, plugin_names):
            model_name = model_dotted_path.split(".")[-1]

            if is_create_or_update:
                dotted_path = f"labelit.plugins.{plugin_name}.serializers.CreateOrUpdate{model_name}Serializer"
            else:
                dotted_path = (
                    f"labelit.plugins.{plugin_name}.serializers.{model_name}Serializer"
                )
            try:
                resolve(dotted_path)
            except ModuleNotFoundError:
                print(
                    f"Module not found !! Plugin: {plugin_name}, dotted path: {dotted_path}"
                )
                continue

            serializer_dotted_paths.append(dotted_path)
            corresponding_model_dotted_paths.append(model_dotted_path)
        return serializer_dotted_paths, corresponding_model_dotted_paths

    serializer_dotted_paths, model_dotted_paths = _get_serializer_dotted_paths()

    return {
        resolve(model_dotted_path): resolve(serializer_dotted_path)
        for (serializer_dotted_path, model_dotted_path) in zip(
            serializer_dotted_paths, model_dotted_paths
        )
    }
