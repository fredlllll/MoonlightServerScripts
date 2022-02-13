class SettingsMeta(type):
    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        cls.__modules = []

    def register_module_or_dict(cls, mod) -> None:
        cls.__modules.insert(0, mod)

    def __getattr__(cls, item):
        for mod in cls.__modules:
            if isinstance(mod, dict):
                if item in mod:
                    return mod[item]
            else:
                if item in mod.__dict__:
                    return getattr(mod, item)
        return super().__getattribute__(item)

    def list_settings_names(cls) -> set:
        retval = set()
        for mod in cls.__modules:
            if isinstance(mod, dict):
                for item in mod:
                    retval.add(item)
            else:
                for item in mod.__dict__:
                    if '__' not in item:
                        retval.add(item)
        return retval


class Settings(metaclass=SettingsMeta):
    pass
