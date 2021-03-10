import json
import logging

from ..BaseHandlerProvider import get_base_handler

logger = logging.getLogger(__name__)


class APIHandler(get_base_handler()):
    url = '/api/(?P<api_name>[^/]+)/(?P<method_name>[^/]+)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._named_apis = {}

    def _add_api(self, named_api):
        self._named_apis[named_api.api_name] = named_api

    def post(self, *args, **kwargs):
        api_name = kwargs.get('api_name', None)
        named_api = self._named_apis.get(api_name, None)
        if named_api is None:
            return self.do_404()

        method_name = kwargs.get('method_name', None)
        if method_name == '__init__':
            return self.do_403()

        named_method = getattr(named_api, method_name, None)
        if named_method is None:
            return self.do_404()

        logger.info("API " + api_name + "/" + method_name + " getting called")
        result = named_method(self)

        self.write(json.dumps(result))
        self.finish()

    def do_404(self, msg="The api or method you requested was not found"):
        self.set_status(404, msg)
        self.write(msg)
        self.finish()

    def do_403(self, msg="You have to be logged in to use this api method"):
        self.set_status(403, msg)
        self.write(msg)
        self.finish()
