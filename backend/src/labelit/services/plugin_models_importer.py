import os
from pkgutil import iter_modules
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module


def import_plugin_models(
    globals_dict: dict,
):
    """
    Automatically imports model classes from plugins.
    This is to be used in models/__init__.py to automatically
    import expose model classes

    Args:
        globals_dict: pass globals() from models/__init__.py

    Returns:
        None
    """
    # iterate through the plugins
    here = os.path.abspath(os.path.dirname(__file__))
    plugins_path = os.path.join(here, "../plugins")
    for plugin_name in os.listdir(plugins_path):
        # iterate through the models package
        models_package_path = os.path.join(plugins_path, plugin_name, "models")
        for _, module_name, _ in iter_modules([models_package_path]):
            # import the module and iterate through its attributes
            module = import_module(
                f"labelit.plugins.{plugin_name}.models.{module_name}"
            )
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)

                if isclass(attribute):
                    # Add the class to this package's variables
                    globals_dict[attribute_name] = attribute
