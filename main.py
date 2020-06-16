from TornadoBaseFramework.Settings import Settings
from Settings import AppSettings

Settings.register_module(AppSettings)
try:
    import LocalSettings

    Settings.register_module(LocalSettings)
except Exception as e:
    print(str(e))

from TornadoBaseFramework.Logging import init_logging

init_logging()

import logging

logger = logging.getLogger(__name__)
logger.info("Moonlight dashboard Startup")

from TornadoBaseFramework.TornadoApplication import TornadoApplication

logger.info("Creating Tornado Applications")
app = TornadoApplication(Settings.TORNADO_APPLICATIONS['tornado'])

logger.info("Adding Pages")
from Handlers.AppPages import pages

for page in pages:
    app.add_handler(page.url, page)

logger.info("Starting app")
app.start()
app.run_loop()
