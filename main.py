from Framework.Logging import init_logging

init_logging()

import logging

logger = logging.getLogger(__name__)
logger.info("Moonlight dashboard Startup")

from Framework.TornadoApplication import TornadoApplication

from Handlers.AppPages import pages

logger.info("Creating Tornado Applications")
app = TornadoApplication()

logger.info("Adding Pages")

for page in pages:
    app.add_handler(page.url_pattern, page)

logger.info("Starting app")
app.start()
app.run_loop()
