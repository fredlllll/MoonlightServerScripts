from .SelectiveIterator import SelectiveIterator


class MicroMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_selective_iterator(self, fields):
        return SelectiveIterator(self, fields)
