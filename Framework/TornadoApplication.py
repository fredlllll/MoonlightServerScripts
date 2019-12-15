import os

import tornado.ioloop
from tornado.web import Application
from tornado import httpserver

from Handlers.Pages.DefaultHandler import DefaultHandler
from Handlers.BetterStaticFileHandler import BetterStaticFileHandler
import Settings.Settings
import logging

import asyncio

try:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # fix for python 3.8 on windows
except:
    pass  # we dont have to do anything on linux and this will fail

logger = logging.getLogger(__name__)


# caps classes for config
class HTTPS_ENDPOINT:
    def __init__(self, enabled, port, certfile, keyfile):
        self.enabled = enabled
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile


class HTTP_ENDPOINT:
    def __init__(self, enabled, port):
        self.enabled = enabled
        self.port = port


class TORNADO_APPLICATION:
    def __init__(self, cookie_secret, endpoints):
        self.cookie_secret = cookie_secret
        self.endpoints = endpoints


class TornadoApplication:
    def __init__(self, handlers=None, ui_modules=None, config_name="tornado"):
        self.app = None
        self.handlers = handlers or []
        self.config_name = config_name
        self.ui_modules = ui_modules or {}
        self.endpoints = []

    def add_handler(self, regex, handler_class):
        self.handlers.append((regex, handler_class))

    def start(self):
        if self.app is None:
            config = Settings.Settings.TORNADO_APPLICATIONS[self.config_name]

            settings = {
                "default_handler_class": DefaultHandler,
                "template_path": os.path.abspath("./templates"),
                "login_url": "/login_signup",
                "cookie_secret": config.cookie_secret,
                "ui_modules": self.ui_modules
            }
            self.app = Application(self.handlers, static_path="./static", static_handler_class=BetterStaticFileHandler, **settings)

            for endp in config.endpoints:
                if isinstance(endp, HTTP_ENDPOINT):
                    if endp.enabled:
                        endpoint = tornado.httpserver.HTTPServer(self.app)
                        port = endp.port
                        logger.info("Starting http on " + str(port))
                        endpoint.listen(port)
                        self.endpoints.append(endpoint)
                elif isinstance(endp, HTTPS_ENDPOINT):
                    if endp.enabled:
                        endpoint = tornado.httpserver.HTTPServer(self.app, ssl_options={
                            "certfile": endp.certfile,
                            "keyfile": endp.keyfile,
                        })
                        port = endp.port
                        logger.info("Starting https on " + str(port))
                        endpoint.listen(port)
                        self.endpoints.append(endpoint)
        else:
            raise Exception("App is already started")

    def run_loop(self):
        tornado.ioloop.IOLoop.instance().start()
