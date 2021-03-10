from TornadoBaseFramework.API.APIHandler import APIHandler


class AppAPIHandler(APIHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # not needing any api yet
