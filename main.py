from lib.settings import Settings
from sanic import Sanic
from sanic.worker.loader import AppLoader
from functools import partial
import logging

logger = logging.getLogger(__name__)
sanic_app = None


def create_app():
    app = Sanic("sanic")
    from lib.sanic_app import SanicApp
    logger.info("Creating App")
    global sanic_app
    sanic_app = SanicApp(app)
    logger.info("Setting up App")
    sanic_app.setup()
    return app


def warmup():
    import os
    import json
    with open('settings.json', 'r') as f:
        Settings.register_module_or_dict(json.load(f))
    if os.path.exists('local_settings.json'):
        with open('local_settings.json', 'r') as f:
            Settings.register_module_or_dict(json.load(f))

    from lib.log import init_logging
    init_logging()


def main():
    warmup()
    loader = AppLoader(factory=partial(create_app))
    app = loader.load()
    logger.info("Running App")
    sanic_app.run(loader)


if __name__ == '__main__':
    main()
else:
    warmup()
