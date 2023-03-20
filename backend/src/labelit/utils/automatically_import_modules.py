from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module


def automatically_import_modules(
    package_dir_path: str,
    name: str,
    globals_dict: dict,
):
    # iterate through the modules in the package
    # package_dir = Path(__file__).resolve().parent
    for _, module_name, _ in iter_modules([package_dir_path]):
        # import the module and iterate through its attributes
        module = import_module(f"{name}.{module_name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute):
                # Add the class to this package's variables
                globals_dict[attribute_name] = attribute
