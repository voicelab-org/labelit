class DatasetImporter:
    def __init__(
        self,
        path_to_uploaded_directory: str,
    ):
        self.dir_path = path_to_uploaded_directory

    def _validate(self):
        raise NotImplementedError

    def _import(self):
        raise NotImplementedError

    def import_dataset(self):
        self._validate()
        self._import()
