import requests
import logging
from Settings.Settings import WEBHOOKS

logger = logging.getLogger(__name__)


class WebhookHandlerDescriptor:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class Webhooks:
    _handlers = {}

    @classmethod
    def add_handler(cls, handler_descriptor):
        handlers = cls._handlers.get(handler_descriptor.name, None)
        if handlers is None:
            handlers = []
            cls._handlers[handler_descriptor.name] = handlers
        handlers.append(handler_descriptor)

    @classmethod
    def trigger(cls, hook_name, hook_data=None):
        handlers = cls._handlers.get(hook_name, None)
        if handlers is not None:
            for handler in handlers:
                try:
                    with requests.post(handler.url, data=hook_data, stream=True) as _:
                        pass
                except Exception as ex:
                    logger.warning("Error when invoking webhook " + hook_name + " to " + handler.url + " with Exception: " + str(ex))


for name, hooks in WEBHOOKS.items():
    for hook in hooks:
        if hook["enabled"]:
            Webhooks.add_handler(WebhookHandlerDescriptor(name, hook["url"]))
