from Util import is_string_truthy

OPTION_TYPE_BOOLEAN = 'bool'


class Option:
    def __init__(self, name, kwargs_name, default, _type=OPTION_TYPE_BOOLEAN):
        self.name = name
        self.kwargs_name = kwargs_name
        self.default = default
        self.value = default
        self.type = _type

    def choose(self):
        chosen = input(self.name + ", Default: '" + str(self.default) + "'? (y/n/empty means default):")
        if len(chosen) > 0:
            self.value = is_string_truthy(chosen)
        else:
            self.value = self.default


class ChooseOptions:
    def __init__(self, options):
        self.options = options

    def choose_options(self):
        print("options:\n")
        kwargs = {}
        for opt in self.options:
            opt.choose()
            kwargs[opt.kwargs_name] = opt.value
        return kwargs
