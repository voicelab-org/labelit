def create_polymorphic_serializer_mapping(
    is_create_or_update=False,
    is_task_mapping=True,
):
    if is_task_mapping:
        model_type_name = "task"
    else:
        model_type_name = "label"

    def _get_dotted_paths():
        def _get_model_names():
            model_filenames = list(
                filter(
                    lambda fname: fname.endswith(f"{model_type_name}.py"),
                    os.listdir(
                        os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            f"../models/{model_type_name}_types",
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

            return list(map(_model_file_name_to_class_name, model_filenames))

        model_names = _get_model_names()

        return list(map(lambda name: f"labelit.models.{name}", model_names))

    model_dotted_paths = _get_dotted_paths()

    def _get_serializer_dotted_paths():
        serializer_dotted_paths = []
        corresponding_model_dotted_paths = []
        for model_dotted_path in model_dotted_paths:
            model_name = model_dotted_path.split(".")[-1]
            if model_type_name == "label":
                model_name = model_name.replace("Task", "Label")

            if is_create_or_update:
                dotted_path = f"labelit.{model_type_name}_types.serializers.CreateOrUpdate{model_name}Serializer"
            else:
                dotted_path = f"labelit.{model_type_name}_types.serializers.{model_name}Serializer"
            try:
                resolve(dotted_path)
            except ModuleNotFoundError:
                continue
            serializer_dotted_paths.append(dotted_path)
            corresponding_model_dotted_paths.append(model_dotted_paths)
        return (serializer_dotted_paths, model_dotted_paths)

    serializer_dotted_paths, model_dotted_paths = _get_serializer_dotted_paths()

    return {
        resolve(model_dotted_path): resolve(serializer_dotted_path)
        for (serializer_dotted_path, model_dotted_path) in zip(
            serializer_dotted_paths, model_dotted_paths
        )
    }
