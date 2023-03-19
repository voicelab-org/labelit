from pathlib import Path
from labelit.utils.automatically_import_modules import automatically_import_modules

print("globals() before", globals())

package_dir_path = Path(__file__).resolve().parent
dunder_name = __name__
automatically_import_modules(
    package_dir_path,
    dunder_name,
    globals(),
)

print("globals() after", globals())