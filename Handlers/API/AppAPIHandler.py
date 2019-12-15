from Framework.API.APIHandler import APIHandler
from Handlers.API.UserAPI import UserAPI


class AppAPIHandler(APIHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # not needing any api yet
        # self._add_api(UserAPI())
