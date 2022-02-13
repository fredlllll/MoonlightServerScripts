import logging
import asyncio
import time

logger = logging.getLogger(__name__)


class LogTimestamper:
    def __init__(self, interval=60):
        self.interval = interval

    def start(self, sanic_app):
        logger.info("Timestamper start")
        sanic_app.add_task(self._run())

    def get_formatted_now(self):
        t = time.time()
        return time.strftime("%Y.%m.%d-%H:%M:%S", time.gmtime(t))

    async def _run(self):
        while True:
            logger.info("[TIMESTAMP]: " + self.get_formatted_now())
            await asyncio.sleep(self.interval)
