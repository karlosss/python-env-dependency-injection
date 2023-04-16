from typing import Any
import importlib


def import_string(path: str) -> Any:
    module_path, object_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, object_name)
