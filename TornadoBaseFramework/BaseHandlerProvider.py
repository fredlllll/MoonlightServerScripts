from importlib import import_module
from .Settings import Settings


def get_base_handler():
    class_path: str = Settings.BASE_HANDLER_CLASS
    last_dot = class_path.rfind('.')

    first_part = class_path[0:last_dot]
    second_part = class_path[last_dot + 1:]

    mod = import_module(first_part)
    my_class = getattr(mod, second_part)
    return my_class
