class SettingsMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.__modules = []

    def register_module(cls, mod):
        cls.__modules.insert(0, mod)

    def __getattr__(cls, item):
        for mod in cls.__modules:
            if item in mod.__dict__:
                return getattr(mod, item)
        return super().__getattribute__(item)


class Settings(metaclass=SettingsMeta):
    pass
