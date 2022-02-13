import logging
import threading
import time

logger = logging.getLogger(__name__)


class LogTimestamper:
    def __init__(self, interval=60):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.interval = interval

    def start(self):
        logger.info("Timestamper start")
        self.thread.start()

    def get_formatted_now(self):
        t = time.time()
        return time.strftime("%Y.%m.%d-%H:%M:%S", time.gmtime(t))

    def _run(self):
        while True:
            logger.info("[TIMESTAMP]: " + self.get_formatted_now())
            time.sleep(self.interval)
