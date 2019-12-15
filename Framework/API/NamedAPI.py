import json


class NamedAPI:
    def __init__(self, api_name):
        self.api_name = api_name  #

    def get_arg(self, handler):
        arg = handler.get_argument('a', None)
        if arg is not None:
            return json.loads(arg)
        return None
