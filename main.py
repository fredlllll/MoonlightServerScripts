from lib.settings import Settings


def main():
    import os
    import json
    with open('settings.json', 'r') as f:
        Settings.register_module_or_dict(json.load(f))
    if os.path.exists('local_settings.json'):
        with open('local_settings.json', 'r') as f:
            Settings.register_module_or_dict(json.load(f))

    from lib.log import init_logging
    init_logging()

    import logging
    logger = logging.getLogger(__name__)

    from lib.sanic_app import SanicApp
    logger.info("Creating App")
    app = SanicApp()
    logger.info("Setting up App")
    app.setup()
    logger.info("Running App")
    app.run()


if __name__ == '__main__':
    main()
