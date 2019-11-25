from ChooseOptions import ChooseOptions
from Util import try_parse_int


class Method:
    def __init__(self, name, method, options=None):
        self.name = name
        self.method = method
        if options is not None:
            self.options = options
        else:
            self.options = []

    def run(self):
        # check optionss
        choose_opts = ChooseOptions(self.options)
        kwargs = choose_opts.choose_options()
        return self.method(**kwargs)


class ChooseMethod:
    def __init__(self, methods):
        self.methods = methods

    def choose(self):
        method_count = len(self.methods)
        if method_count == 0:
            print("No methods found to execute")
            return

        print("Available methods are:\n")
        for i in range(method_count):
            print(str(i) + ') ' + self.methods[i].name)
        chosen_method = try_parse_int(input("Choose method:"))

        if chosen_method is not None:
            return self.methods[chosen_method].run()
        return None
