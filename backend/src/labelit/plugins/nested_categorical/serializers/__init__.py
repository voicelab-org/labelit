from pathlib import Path
from labelit.utils.automatically_import_module_classes import (
    automatically_import_module_classes,
)

package_dir_path = Path(__file__).resolve().parent
dunder_name = __name__
automatically_import_module_classes(
    package_dir_path,
    dunder_name,
    globals(),
)
